"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Calendar as CalendarIcon, Clock, Globe, Sparkles, CheckCircle2, ArrowRight, ShieldCheck, Mail, AlertCircle } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { loadQuestionnaire } from "@/lib/storage";
import { QuestionnaireData } from "@/types/questionnaire";

interface BookingRecord {
  id: string;
  userName: string;
  userEmail: string;
  date: string;
  timeSlot: string;
  timezone: string;
  status: "confirmed";
  createdAt: string;
}

const BOOKING_STORAGE_KEY = "converse_ai_manifest_booking";

export default function BookingPage() {
  const router = useRouter();
  const [questionnaire, setQuestionnaire] = useState<QuestionnaireData | null>(null);
  const [userTimezone, setUserTimezone] = useState("UTC");
  const [selectedDateIndex, setSelectedDateIndex] = useState(0);
  const [selectedSlot, setSelectedSlot] = useState<string>("");
  const [confirmedBooking, setConfirmedBooking] = useState<BookingRecord | null>(null);
  const [isBooking, setIsBooking] = useState(false);

  // Generate 6 upcoming days starting today
  const availableDates = Array.from({ length: 6 }, (_, i) => {
    const d = new Date();
    d.setDate(d.getDate() + i);
    return {
      iso: d.toISOString().split("T")[0],
      dayName: i === 0 ? "Today" : i === 1 ? "Tomorrow" : d.toLocaleDateString("en-US", { weekday: "short" }),
      formattedDate: d.toLocaleDateString("en-US", { month: "short", day: "numeric" }),
    };
  });

  const timeSlots = [
    { label: "Morning Ceremony", slots: ["09:30 AM", "10:15 AM", "11:00 AM", "11:45 AM"] },
    { label: "Afternoon Reflection", slots: ["02:00 PM", "02:45 PM", "03:30 PM", "04:15 PM"] },
    { label: "Evening Grounding", slots: ["06:00 PM", "06:45 PM", "07:30 PM", "08:15 PM", "09:00 PM"] },
  ];

  useEffect(() => {
    const q = loadQuestionnaire();
    setQuestionnaire(q);

    // Auto-detect browser timezone
    try {
      const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
      setUserTimezone(tz || "UTC");
    } catch {
      setUserTimezone("UTC");
    }

    // Check if user already booked
    const saved = localStorage.getItem(BOOKING_STORAGE_KEY);
    if (saved) {
      try {
        setConfirmedBooking(JSON.parse(saved));
      } catch (e) {
        console.error("Failed to parse booking", e);
      }
    }
  }, []);

  const handleConfirmBooking = () => {
    if (!selectedSlot) return;

    setIsBooking(true);
    const chosenDate = availableDates[selectedDateIndex];

    const booking: BookingRecord = {
      id: "book_" + Math.random().toString(36).substring(2, 9),
      userName: questionnaire?.fullName || "Friend",
      userEmail: questionnaire?.email || "",
      date: `${chosenDate.dayName}, ${chosenDate.formattedDate}`,
      timeSlot: selectedSlot,
      timezone: userTimezone,
      status: "confirmed",
      createdAt: new Date().toISOString(),
    };

    setTimeout(() => {
      localStorage.setItem(BOOKING_STORAGE_KEY, JSON.stringify(booking));
      setConfirmedBooking(booking);
      setIsBooking(false);
    }, 600);
  };

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center space-y-3">
        <Badge variant="gold" className="mx-auto">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Step 2 • Dedicated Appointment Scheduling</span>
        </Badge>
        <h1 className="font-serif text-3xl sm:text-5xl font-bold" style={{ color: "var(--color-text)" }}>
          Book Your Hero Voice Session
        </h1>
        <p className="text-xs sm:text-sm max-w-lg mx-auto" style={{ color: "var(--color-muted)" }}>
          Your coordinates are saved. Select an intimate time slot to speak out loud with Hero in real time.
        </p>

        {questionnaire?.email && (
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs" style={{ background: "var(--color-card)", border: "1px solid var(--color-border)", color: "var(--color-text)" }}>
            <Mail className="w-3.5 h-3.5" style={{ color: "var(--color-accent)" }} />
            <span>Booking confirmation will be sent to: <strong>{questionnaire.email}</strong></span>
          </div>
        )}
      </div>

      {/* If Booking is Confirmed */}
      {confirmedBooking ? (
        <Card variant="default" className="p-8 sm:p-12 text-center space-y-6 max-w-2xl mx-auto animate-in fade-in duration-400">
          <div className="w-16 h-16 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center mx-auto text-emerald-400">
            <CheckCircle2 className="w-8 h-8" />
          </div>

          <div className="space-y-2">
            <Badge variant="champagne">Ceremony Confirmed</Badge>
            <h2 className="font-serif text-3xl font-bold" style={{ color: "var(--color-text)" }}>
              You Are Booked with Hero
            </h2>
            <p className="text-sm" style={{ color: "var(--color-muted)" }}>
              Hero has reserved your dedicated voice sanctuary.
            </p>
          </div>

          {/* Booking Summary Box */}
          <div className="p-6 rounded-2xl text-left space-y-3 max-w-md mx-auto" style={{ background: "rgba(0,0,0,0.25)", border: "1px solid var(--color-border)" }}>
            <div className="flex items-center justify-between text-xs pb-2 border-b" style={{ borderColor: "var(--color-border)" }}>
              <span style={{ color: "var(--color-muted)" }}>Attendee:</span>
              <span className="font-bold" style={{ color: "var(--color-text)" }}>{confirmedBooking.userName}</span>
            </div>
            <div className="flex items-center justify-between text-xs pb-2 border-b" style={{ borderColor: "var(--color-border)" }}>
              <span style={{ color: "var(--color-muted)" }}>Scheduled Date:</span>
              <span className="font-bold" style={{ color: "var(--color-text)" }}>{confirmedBooking.date}</span>
            </div>
            <div className="flex items-center justify-between text-xs pb-2 border-b" style={{ borderColor: "var(--color-border)" }}>
              <span style={{ color: "var(--color-muted)" }}>Time Slot:</span>
              <span className="font-bold text-emerald-400">{confirmedBooking.timeSlot} ({confirmedBooking.timezone})</span>
            </div>
            <div className="flex items-center justify-between text-xs">
              <span style={{ color: "var(--color-muted)" }}>Max Duration:</span>
              <span className="font-bold" style={{ color: "var(--color-text)" }}>9 Minutes (Ceremonial Dialogue)</span>
            </div>
          </div>

          {/* Action CTAs */}
          <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/call" className="w-full sm:w-auto">
              <Button size="lg" variant="primary" className="w-full sm:w-auto">
                <span>Enter Call Sanctuary (Join Now)</span>
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </Link>
            <Button
              size="lg"
              variant="outline"
              onClick={() => {
                localStorage.removeItem(BOOKING_STORAGE_KEY);
                setConfirmedBooking(null);
              }}
              className="w-full sm:w-auto"
            >
              <span>Reschedule Slot</span>
            </Button>
          </div>

          <p className="text-xs italic" style={{ color: "var(--color-muted)" }}>
            &quot;Consider your manifestation ready. We&apos;ll come back within 15 days with a surprise.&quot;
          </p>
        </Card>
      ) : (
        /* Booking Selection Flow */
        <Card variant="default" className="p-6 sm:p-10 space-y-8">
          
          {/* 1. Date Selection Pills */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <label className="text-xs font-semibold uppercase tracking-wider flex items-center gap-1.5" style={{ color: "var(--color-text)" }}>
                <CalendarIcon className="w-4 h-4" style={{ color: "var(--color-accent)" }} />
                <span>Select Appointment Date</span>
              </label>
              <span className="text-xs flex items-center gap-1" style={{ color: "var(--color-muted)" }}>
                <Globe className="w-3.5 h-3.5" />
                {userTimezone}
              </span>
            </div>

            <div className="grid grid-cols-3 sm:grid-cols-6 gap-2.5">
              {availableDates.map((item, idx) => {
                const isSelected = selectedDateIndex === idx;
                return (
                  <button
                    key={item.iso}
                    type="button"
                    onClick={() => {
                      setSelectedDateIndex(idx);
                      setSelectedSlot("");
                    }}
                    className={`p-3 rounded-2xl flex flex-col items-center justify-center text-center transition-all duration-200 border ${
                      isSelected
                        ? "bg-purple-600 text-white border-purple-400 shadow-lg scale-105"
                        : "hover:bg-white/10"
                    }`}
                    style={!isSelected ? { background: "var(--color-card)", borderColor: "var(--color-border)", color: "var(--color-text)" } : {}}
                  >
                    <span className="text-[11px] font-semibold uppercase">{item.dayName}</span>
                    <span className="text-sm font-bold mt-0.5">{item.formattedDate}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* 2. Time Slot Selection Grid */}
          <div className="space-y-6">
            <label className="text-xs font-semibold uppercase tracking-wider flex items-center gap-1.5" style={{ color: "var(--color-text)" }}>
              <Clock className="w-4 h-4" style={{ color: "var(--color-accent)" }} />
              <span>Select 15-Minute Time Slot ({availableDates[selectedDateIndex].dayName})</span>
            </label>

            {timeSlots.map((section) => (
              <div key={section.label} className="space-y-2">
                <span className="text-xs font-medium uppercase tracking-wider" style={{ color: "var(--color-muted)" }}>
                  {section.label}
                </span>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                  {section.slots.map((slot) => {
                    const isSelected = selectedSlot === slot;
                    return (
                      <button
                        key={slot}
                        type="button"
                        onClick={() => setSelectedSlot(slot)}
                        className={`py-2.5 px-4 rounded-xl text-xs font-semibold border transition-all duration-200 ${
                          isSelected
                            ? "bg-emerald-600 text-white border-emerald-400 shadow-md scale-102"
                            : "hover:border-purple-400"
                        }`}
                        style={!isSelected ? { background: "var(--color-card)", borderColor: "var(--color-border)", color: "var(--color-text)" } : {}}
                      >
                        {slot}
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>

          {/* 3. Confirm Button */}
          <div className="pt-6 border-t flex flex-col sm:flex-row items-center justify-between gap-4" style={{ borderColor: "var(--color-border)" }}>
            <div className="text-xs" style={{ color: "var(--color-muted)" }}>
              {selectedSlot ? (
                <span>Selected: <strong style={{ color: "var(--color-text)" }}>{availableDates[selectedDateIndex].dayName}, {selectedSlot}</strong></span>
              ) : (
                <span>Please select a time slot above to confirm your session.</span>
              )}
            </div>

            <Button
              variant="primary"
              size="lg"
              disabled={!selectedSlot || isBooking}
              isLoading={isBooking}
              onClick={handleConfirmBooking}
            >
              <span>Confirm & Lock Appointment</span>
              <ArrowRight className="w-4 h-4 ml-1.5" />
            </Button>
          </div>
        </Card>
      )}
    </div>
  );
}
