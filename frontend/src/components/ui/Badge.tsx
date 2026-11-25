import React from "react";
import { cn } from "@/lib/utils";

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "lavender" | "blush" | "peach" | "sky" | "champagne" | "gold";
}

export function Badge({
  className,
  variant = "lavender",
  children,
  ...props
}: BadgeProps) {
  const variants = {
    lavender: "bg-dream-lavender/60 text-dream-plum border-dream-lavender-dark/40",
    blush: "bg-dream-blush/60 text-dream-plum border-dream-blush-dark/40",
    peach: "bg-dream-peach/60 text-dream-plum border-dream-peach-dark/40",
    sky: "bg-dream-sky/60 text-dream-plum border-dream-sky-dark/40",
    champagne: "bg-dream-champagne/60 text-dream-plum border-dream-champagne-dark/40",
    gold: "bg-[#FBF4E4] text-[#8C6D1F] border-[#E5D298]",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border tracking-wide uppercase",
        variants[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}
