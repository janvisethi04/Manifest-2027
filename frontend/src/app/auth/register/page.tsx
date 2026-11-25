"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Sparkles, ArrowRight, User, Mail, Lock, ShieldCheck } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";

export default function RegisterPage() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert("Phase 1 Preview: Full registration and multi-step questionnaire will be activated in Phase 2.");
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center px-4 py-16">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center space-y-2">
          <Badge variant="gold" className="mx-auto">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Begin Your Manifestation</span>
          </Badge>
          <h1 className="font-serif text-3xl sm:text-4xl font-bold text-dream-plum">
            Create Your Sanctuary Account
          </h1>
          <p className="text-xs sm:text-sm text-dream-plum-muted">
            Step into 2027. Your answers and voice conversations remain private, secure, and uniquely yours.
          </p>
        </div>

        <Card variant="default" className="bg-white/90 p-8 shadow-dreamy-lg border-dream-lavender">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-dream-plum mb-1.5">
                Your Full / Preferred Name
              </label>
              <div className="relative">
                <User className="absolute left-3.5 top-3 w-4 h-4 text-dream-plum-muted" />
                <input
                  type="text"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Sarah Jenkins"
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-dream-lavender/60 bg-dream-ivory text-sm text-dream-plum focus:ring-2 focus:ring-dream-lavender-dark focus:outline-none transition-all"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-dream-plum mb-1.5">
                Email Address
              </label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-3 w-4 h-4 text-dream-plum-muted" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="sarah@manifest2027.com"
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-dream-lavender/60 bg-dream-ivory text-sm text-dream-plum focus:ring-2 focus:ring-dream-lavender-dark focus:outline-none transition-all"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-dream-plum mb-1.5">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3.5 top-3 w-4 h-4 text-dream-plum-muted" />
                <input
                  type="password"
                  required
                  minLength={8}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="At least 8 characters"
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-dream-lavender/60 bg-dream-ivory text-sm text-dream-plum focus:ring-2 focus:ring-dream-lavender-dark focus:outline-none transition-all"
                />
              </div>
            </div>

            <div className="flex items-center gap-2 text-xs text-dream-plum-muted pt-1">
              <ShieldCheck className="w-4 h-4 text-emerald-600 flex-shrink-0" />
              <span>Argon2id encrypted passwords & secure session cookies</span>
            </div>

            <Button type="submit" variant="primary" className="w-full justify-center mt-2">
              <span>Continue to Questionnaire</span>
              <ArrowRight className="w-4 h-4 ml-1.5" />
            </Button>
          </form>

          <div className="mt-6 pt-6 border-t border-dream-lavender/40 text-center text-xs text-dream-plum-muted">
            <span>Already have an account? </span>
            <Link href="/auth/login" className="font-semibold text-dream-plum underline hover:text-dream-plum-light">
              Sign In
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
}
