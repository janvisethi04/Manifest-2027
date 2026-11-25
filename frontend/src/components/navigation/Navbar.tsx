"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Sparkles, Menu, X, ArrowRight, Heart } from "lucide-react";
import { Button } from "@/components/ui/Button";

export function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full transition-all duration-300">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-4">
        <div className="relative flex items-center justify-between h-16 px-6 bg-white/70 backdrop-blur-md rounded-full border border-white/60 shadow-dreamy">
          {/* Brand Logo */}
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="relative flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-tr from-dream-lavender via-dream-blush to-dream-champagne border border-white shadow-sm transition-transform duration-300 group-hover:scale-105">
              <Sparkles className="w-5 h-5 text-dream-plum transition-transform duration-300 group-hover:rotate-12" />
            </div>
            <div className="flex flex-col">
              <span className="font-serif text-xl font-bold tracking-tight text-dream-plum leading-none">
                Converse AI
              </span>
              <span className="text-[10px] tracking-widest uppercase text-dream-plum-muted font-medium">
                Manifest 2027
              </span>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-dream-plum/80">
            <Link
              href="/questionnaire"
              className="hover:text-purple-400 transition-colors hover:-translate-y-0.5 transform duration-200"
            >
              1. Questionnaire
            </Link>
            <Link
              href="/booking"
              className="hover:text-purple-400 transition-colors hover:-translate-y-0.5 transform duration-200"
            >
              2. Book Slot
            </Link>
            <Link
              href="/call"
              className="hover:text-purple-400 transition-colors hover:-translate-y-0.5 transform duration-200"
            >
              3. Talk to Hero
            </Link>
            <Link
              href="/board"
              className="hover:text-purple-400 transition-colors hover:-translate-y-0.5 transform duration-200"
            >
              4. Miro Board
            </Link>
          </nav>

          {/* Desktop Actions */}
          <div className="hidden md:flex items-center gap-3">
            <Link href="/questionnaire">
              <Button variant="primary" size="sm">
                <span>Begin Your 2027</span>
                <ArrowRight className="w-3.5 h-3.5 ml-1" />
              </Button>
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <div className="flex md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-full text-dream-plum hover:bg-dream-lavender/40 transition-colors"
              aria-label="Toggle navigation menu"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden mx-4 mt-2 p-6 bg-white/95 backdrop-blur-xl rounded-3xl border border-dream-lavender shadow-dreamy-lg flex flex-col gap-4 animate-in fade-in slide-in-from-top-4 duration-300">
          <nav className="flex flex-col gap-3 text-base font-medium text-dream-plum">
            <Link
              href="/questionnaire"
              onClick={() => setMobileMenuOpen(false)}
              className="py-2 px-3 rounded-xl hover:bg-dream-lavender/30"
            >
              1. Questionnaire
            </Link>
            <Link
              href="/call"
              onClick={() => setMobileMenuOpen(false)}
              className="py-2 px-3 rounded-xl hover:bg-dream-lavender/30"
            >
              2. Talk to Hero
            </Link>
            <Link
              href="/board"
              onClick={() => setMobileMenuOpen(false)}
              className="py-2 px-3 rounded-xl hover:bg-dream-lavender/30"
            >
              3. Manifestation Board
            </Link>
          </nav>

          <div className="h-px bg-dream-lavender/50 my-1" />

          <div className="flex flex-col gap-2.5">
            <Link href="/questionnaire" onClick={() => setMobileMenuOpen(false)}>
              <Button variant="primary" className="w-full justify-center">
                <span>Begin Your 2027</span>
                <ArrowRight className="w-4 h-4 ml-1.5" />
              </Button>
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
