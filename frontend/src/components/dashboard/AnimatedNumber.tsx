import { useEffect, useState, useRef, useCallback } from "react";
import { memo } from "react";

interface AnimatedNumberProps {
  targetValue: number;
  duration?: number;
  delay?: number;
  className?: string;
  showPercentage?: boolean;
  formatValue?: (value: number) => string;
}

// Session storage key for tracking animated components
const SESSION_ANIMATION_KEY = "animated_numbers_session";

const AnimatedNumber = memo(
  ({
    targetValue,
    duration = 1000,
    delay = 0,
    className = "",
    showPercentage = false,
    formatValue,
  }: AnimatedNumberProps) => {
    const [currentValue, setCurrentValue] = useState(0);
    const animationId = useRef<string>(`${targetValue}_${duration}_${delay}`);
    const hasRunRef = useRef(false);

    // Function to check if animation should run
    const shouldAnimate = useCallback(() => {
      // If we've already run in this component instance, don't run again
      if (hasRunRef.current) return false;

      const sessionData = sessionStorage.getItem(SESSION_ANIMATION_KEY);
      if (!sessionData) return true; // No session data, allow animation

      const animatedComponents = JSON.parse(sessionData);
      return !animatedComponents[animationId.current];
    }, []);

    // Function to mark animation as completed
    const markAnimationComplete = useCallback(() => {
      hasRunRef.current = true;
      const sessionData = sessionStorage.getItem(SESSION_ANIMATION_KEY);
      const animatedComponents = sessionData ? JSON.parse(sessionData) : {};
      animatedComponents[animationId.current] = true;
      sessionStorage.setItem(
        SESSION_ANIMATION_KEY,
        JSON.stringify(animatedComponents)
      );
    }, []);

    // Function to run the animation
    const runAnimation = useCallback(() => {
      const timer = setTimeout(() => {
        const startTime = Date.now();
        const startValue = 0;

        const animate = () => {
          const elapsed = Date.now() - startTime;
          const progress = Math.min(elapsed / duration, 1);

          // Easing function for smooth animation
          const easeOutQuart = 1 - Math.pow(1 - progress, 4);
          const newValue =
            startValue + (targetValue - startValue) * easeOutQuart;

          setCurrentValue(Math.round(newValue));

          if (progress < 1) {
            requestAnimationFrame(animate);
          } else {
            // Animation completed - mark it as done in session storage
            markAnimationComplete();
          }
        };

        animate();
      }, delay);

      return () => clearTimeout(timer);
    }, [targetValue, duration, delay, markAnimationComplete]);

    useEffect(() => {
      // Always reset to 0 when component mounts
      setCurrentValue(0);

      // Check if we should animate
      if (shouldAnimate()) {
        // Run the animation (don't mark as complete until it finishes)
        return runAnimation();
      } else {
        // Animation already ran, set to final value immediately
        setCurrentValue(targetValue);
      }
    }, [targetValue, duration, delay, shouldAnimate, runAnimation]);

    const displayValue = formatValue ? formatValue(currentValue) : currentValue;
    const displayText = showPercentage ? `${displayValue}%` : displayValue;

    return <span className={className}>{displayText}</span>;
  }
);

AnimatedNumber.displayName = "AnimatedNumber";

export default AnimatedNumber;
