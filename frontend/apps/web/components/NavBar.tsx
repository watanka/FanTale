"use client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

const links = [
  { href: "/me", label: "내 정보" },
  { href: "/library", label: "내 서재" },
  { href: "/fandoms", label: "팬덤" },
];

export default function NavBar() {
  const pathname = usePathname();
  const router = useRouter();
  const [userName, setUserName] = useState<string | null>(null);

  const readAuth = () => {
    try {
      const raw = localStorage.getItem("fantale_auth");
      if (!raw) {
        setUserName(null);
        return;
      }
      const data = JSON.parse(raw);
      const name = data?.user?.name || data?.user_info?.name || null;
      setUserName(name);
    } catch {
      setUserName(null);
    }
  };

  useEffect(() => {
    readAuth();
  }, [pathname]);

  useEffect(() => {
    const handler = () => readAuth();
    window.addEventListener("fantale-auth-updated", handler);
    return () => window.removeEventListener("fantale-auth-updated", handler);
  }, []);

  const handleLogin = () => {
    // Kick off OAuth flow via backend redirect
    window.location.href = "/api/auth/google/login";
  };

  const handleLogout = async () => {
    try {
      const raw = localStorage.getItem("fantale_auth");
      let payload: any = { provider: "google" };
      if (raw) {
        try {
          const data = JSON.parse(raw);
          payload.access_token = data?.access_token;
          payload.refresh_token = data?.refresh_token;
          payload.id_token = data?.id_token;
        } catch {}
      }
      await fetch("/api/auth/logout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        credentials: "include",
      });
    } catch {}
    localStorage.removeItem("fantale_auth");
    try {
      window.dispatchEvent(new Event("fantale-auth-updated"));
    } catch {}
    setUserName(null);
    router.refresh();
  };

  return (
    <nav className="flex items-center gap-5 text-sm">
      {links.map((l) => {
        const active = pathname === l.href || pathname?.startsWith(l.href + "/");
        return (
          <Link
            key={l.href}
            href={l.href}
            className={
              "group relative transition hover:opacity-90 " +
              (active ? "text-[color:var(--color-brand-main)]" : "")
            }
          >
            <span>{l.label}</span>
            <span
              className={
                "absolute -bottom-1 left-0 h-0.5 w-full origin-left scale-x-0 bg-[color:var(--color-brand-main)] transition-transform duration-200 " +
                (active ? "scale-x-100" : "group-hover:scale-x-100")
              }
            />
          </Link>
        );
      })}
      <div className="ml-2 h-4 w-px bg-black/10 dark:bg-white/10" />
      {userName ? (
        <div className="flex items-center gap-2 text-sm">
          <span className="text-black/70 dark:text-neutral-300">{userName}님</span>
          <button
            onClick={handleLogout}
            className="rounded px-2 py-1 text-xs text-black/70 transition hover:bg-black/5 dark:text-neutral-300 dark:hover:bg-white/10"
          >
            로그아웃
          </button>
        </div>
      ) : (
        <button
          onClick={handleLogin}
          className="rounded bg-[color:var(--color-brand-main)]/10 px-2 py-1 text-xs text-[color:var(--color-brand-main)] transition hover:bg-[color:var(--color-brand-main)]/20"
        >
          로그인
        </button>
      )}
    </nav>
  );
}
