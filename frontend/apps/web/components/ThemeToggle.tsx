"use client";
import { useEffect, useState } from "react";

export default function ThemeToggle() {
  const [mounted, setMounted] = useState(false);
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    setMounted(true);
    const saved = typeof window !== "undefined" ? localStorage.getItem("theme") : null;
    const prefersDark = typeof window !== "undefined" && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const enableDark = saved ? saved === "dark" : prefersDark;
    if (enableDark) {
      document.documentElement.classList.add("dark");
      setIsDark(true);
    } else {
      document.documentElement.classList.remove("dark");
      setIsDark(false);
    }
  }, []);

  const toggle = () => {
    const next = !isDark;
    setIsDark(next);
    if (next) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  };

  if (!mounted) return null;

  return (
    <button
      type="button"
      onClick={toggle}
      aria-label="Toggle dark mode"
      className="inline-flex items-center gap-2 rounded-md border border-black/10 bg-white/70 px-3 py-1.5 text-sm shadow-sm backdrop-blur transition hover:opacity-80 dark:border-white/10 dark:bg-neutral-800 dark:text-white"
    >
      {isDark ? (
        <span className="i-[theme-dark]">🌙</span>
      ) : (
        <span className="i-[theme-light]">☀️</span>
      )}
      <span className="hidden sm:inline">{isDark ? "다크" : "라이트"}</span>
    </button>
  );
}
