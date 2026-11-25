import React from "react";
import Link from "next/link";
import { Sparkles, Heart, Shield, Clock } from "lucide-react";

export function Footer() {
  return (
    <footer className="relative mt-24 border-t border-dream-lavender/50 bg-white/40 backdrop-blur-md">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10">
          {/* Brand Column */}
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center gap-2.5">
              <div className="flex items-center justify-center w-9 h-9 rounded-full bg-gradient-to-tr from-dream-lavender to-dream-blush border border-white shadow-sm">
                <Sparkles className="w-4 h-4 text-dream-plum" />
              </div>
              <span className="font-serif text-2xl font-bold tracking-tight text-dream-plum">
                Converse AI – Manifest 2027
              </span>
            </div>
            <p className="text-sm text-dream-plum-muted max-w-md leading-relaxed">
              An intimate, emotionally intelligent manifestation sanctuary. Powered by conversational voice presence, contextual memory, and bespoke dream boards.
            </p>
            <div className="flex items-center gap-4 text-xs text-dream-plum-muted pt-2">
              <span className="flex items-center gap-1.5">
                <Shield className="w-3.5 h-3.5 text-dream-lavender-dark" />
                Zero-Selling of Personal Data
              </span>
              <span className="flex items-center gap-1.5">
                <Clock className="w-3.5 h-3.5 text-dream-lavender-dark" />
                15-Day Manifestation Surprise
              </span>
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-3">
            <h4 className="font-serif text-base font-semibold text-dream-plum uppercase tracking-wider text-xs">
              Experience
            </h4>
            <ul className="space-y-2 text-sm text-dream-plum-muted">
              <li>
                <Link href="#journey" className="hover:text-dream-plum transition-colors">
                  The 4-Step Journey
                </Link>
              </li>
              <li>
                <Link href="#hero-voice" className="hover:text-dream-plum transition-colors">
                  Hero Companion
                </Link>
              </li>
              <li>
                <Link href="#archetypes" className="hover:text-dream-plum transition-colors">
                  Creative Archetypes
                </Link>
              </li>
              <li>
                <Link href="#board" className="hover:text-dream-plum transition-colors">
                  Manifestation Board
                </Link>
              </li>
            </ul>
          </div>

          {/* Sanctuary Links */}
          <div className="space-y-3">
            <h4 className="font-serif text-base font-semibold text-dream-plum uppercase tracking-wider text-xs">
              Sanctuary
            </h4>
            <ul className="space-y-2 text-sm text-dream-plum-muted">
              <li>
                <Link href="/privacy" className="hover:text-dream-plum transition-colors">
                  Privacy & Data Consent
                </Link>
              </li>
              <li>
                <Link href="/terms" className="hover:text-dream-plum transition-colors">
                  Ethical AI Standards
                </Link>
              </li>
              <li>
                <Link href="/faq" className="hover:text-dream-plum transition-colors">
                  Frequently Asked Questions
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-12 pt-8 border-t border-dream-lavender/40 flex flex-col sm:flex-row items-center justify-between text-xs text-dream-plum-muted gap-4">
          <p>© 2026-2027 Converse AI. Grounded in empathy, elevated by intention.</p>
          <p className="flex items-center gap-1">
            Crafted with <Heart className="w-3.5 h-3.5 text-dream-rose fill-dream-rose/30" /> for your highest self
          </p>
        </div>
      </div>
    </footer>
  );
}
