import "./globals.css";
import type { Metadata } from "next";
import QueryProvider from "../components/QueryProvider";
import Link from "next/link";
import NavBar from "../components/NavBar";
import ThemeToggle from "../components/ThemeToggle";

export const metadata: Metadata = {
  title: "FanTale",
  description: "내 최애와 매일 이어지는 이야기",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko" suppressHydrationWarning>
      <body className="transition-colors duration-200">
        <QueryProvider>
          <div className="min-h-screen bg-bg-soft text-text-dark dark:bg-neutral-950 dark:text-white">
            <header className="sticky top-0 z-40 border-b border-black/5 bg-white/70 backdrop-blur dark:border-white/10 dark:bg-neutral-900/70">
              <div className="mx-auto max-w-[960px] px-4 py-3 flex items-center justify-between">
                <h1 className="text-xl font-semibold">
                  <Link href="/" className="hover:opacity-90">
                    <span className="text-[color:var(--color-brand-main)]">Fan</span>
                    Tale
                  </Link>
                </h1>
                <div className="flex items-center gap-4">
                  <NavBar />
                  <ThemeToggle />
                </div>
              </div>
            </header>
            <main className="mx-auto max-w-[960px] px-4 py-6">{children}</main>
          </div>
        </QueryProvider>
      </body>
    </html>
  );
}
