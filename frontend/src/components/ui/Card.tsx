import React from "react";
import { cn } from "@/lib/utils";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "polaroid" | "glass" | "bordered";
  withTape?: boolean;
}

export function Card({
  className,
  variant = "default",
  withTape = false,
  children,
  ...props
}: CardProps) {
  const variants = {
    default:
      "relative bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-dreamy border border-dream-lavender/40 transition-all duration-300 hover:shadow-dreamy-lg",
    polaroid:
      "relative polaroid-frame bg-white transition-all duration-300",
    glass:
      "relative bg-white/50 backdrop-blur-md rounded-2xl p-6 border border-white/60 shadow-sm",
    bordered:
      "relative bg-dream-ivory rounded-2xl p-6 border border-dream-champagne-dark/30 shadow-sm",
  };

  return (
    <div className={cn(variants[variant], className)} {...props}>
      {withTape && <div className="washi-tape" aria-hidden="true" />}
      {children}
    </div>
  );
}
