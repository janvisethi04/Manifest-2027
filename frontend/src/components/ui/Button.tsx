import React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "gold";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", isLoading = false, children, disabled, ...props }, ref) => {
    const baseStyles =
      "relative inline-flex items-center justify-center font-medium rounded-full transition-all duration-300 ease-out focus:outline-none focus-visible:ring-2 focus-visible:ring-dream-lavender-dark active:scale-[0.98] disabled:opacity-50 disabled:pointer-events-none disabled:active:scale-100 select-none";

    const variants = {
      primary:
        "bg-gradient-to-r from-dream-plum to-dream-plum-light text-white shadow-dreamy hover:shadow-dreamy-lg hover:from-dream-plum-light hover:to-dream-plum hover:-translate-y-0.5",
      secondary:
        "bg-dream-lavender/70 text-dream-plum border border-dream-lavender-dark/50 hover:bg-dream-lavender hover:border-dream-lavender-dark hover:-translate-y-0.5 shadow-sm",
      outline:
        "bg-transparent text-dream-plum border border-dream-plum/20 hover:bg-dream-blush/30 hover:border-dream-plum/40 hover:-translate-y-0.5",
      ghost:
        "bg-transparent text-dream-plum hover:bg-dream-lavender/40 hover:text-dream-plum-light",
      gold:
        "bg-gradient-to-r from-[#D4AF37] to-[#E9D5B0] text-dream-plum font-semibold shadow-gold-glow hover:shadow-lg hover:-translate-y-0.5",
    };

    const sizes = {
      sm: "text-xs px-4 py-1.5 h-8 gap-1.5",
      md: "text-sm px-6 py-2.5 h-11 gap-2",
      lg: "text-base px-8 py-3.5 h-14 gap-2.5",
    };

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={cn(baseStyles, variants[variant], sizes[size], className)}
        {...props}
      >
        {isLoading && (
          <svg
            className="animate-spin -ml-1 mr-2 h-4 w-4 text-current"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        )}
        {children}
      </button>
    );
  }
);

Button.displayName = "Button";
