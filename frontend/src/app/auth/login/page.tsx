"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Sparkles, ArrowRight, Lock, Mail } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert("Phase 1 Preview: Full authentication and session verification will be enabled in Phase 2.");
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4 py-16">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center space-y-2">
          <Badge variant="lavender" className="mx-auto">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Welcome Back</span>
          </Badge>
          <h1 className="font-serif text-3xl sm:text-4xl font-bold text-dream-plum">
            Return to Your Sanctuary
          </h1>
          <p className="text-xs sm:text-sm text-dream-plum-muted">
            Enter your email and password to view your session, questionnaire, or manifestation board.
          </p>
        </div>

        <Card variant="default" className="bg-white/90 p-8 shadow-dreamy-lg border-dream-lavender">
          <form onSubmit={handleSubmit} className="space-y-4">
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
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••••••"
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-dream-lavender/60 bg-dream-ivory text-sm text-dream-plum focus:ring-2 focus:ring-dream-lavender-dark focus:outline-none transition-all"
                />
              </div>
            </div>

            <Button type="submit" variant="primary" className="w-full justify-center mt-2">
              <span>Sign In to Sanctuary</span>
              <ArrowRight className="w-4 h-4 ml-1.5" />
            </Button>
          </form>

          <div className="mt-6 pt-6 border-t border-dream-lavender/40 text-center text-xs text-dream-plum-muted">
            <span>New to Converse AI? </span>
            <Link href="/auth/register" className="font-semibold text-dream-plum underline hover:text-dream-plum-light">
              Create an account
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
}
