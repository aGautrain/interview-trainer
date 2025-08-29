import { useEffect, useState } from "react";

interface AnimatedNumberProps {
  targetValue: number;
  duration?: number;
  delay?: number;
  className?: string;
  showPercentage?: boolean;
  formatValue?: (value: number) => string;
}

const AnimatedNumber = ({
  targetValue,
  duration = 1000,
  delay = 0,
  className = "",
  showPercentage = false,
  formatValue,
}: AnimatedNumberProps) => {
  const [currentValue, setCurrentValue] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      const startTime = Date.now();
      const startValue = 0;

      const animate = () => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Easing function for smooth animation
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        const newValue = startValue + (targetValue - startValue) * easeOutQuart;

        setCurrentValue(Math.round(newValue));

        if (progress < 1) {
          requestAnimationFrame(animate);
        }
      };

      animate();
    }, delay);

    return () => clearTimeout(timer);
  }, [targetValue, duration, delay]);

  const displayValue = formatValue ? formatValue(currentValue) : currentValue;
  const displayText = showPercentage ? `${displayValue}%` : displayValue;

  return <span className={className}>{displayText}</span>;
};

export default AnimatedNumber;
