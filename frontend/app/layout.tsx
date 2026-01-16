import type { Metadata } from 'next';
import { Inter, Outfit } from 'next/font/google';
import './globals.css';
import { dictionary } from '@/lib/dictionary';
import { Scale } from 'lucide-react';

const inter = Inter({ subsets: ['latin', 'latin-ext'], variable: '--font-inter' });
const outfit = Outfit({ subsets: ['latin', 'latin-ext'], variable: '--font-outfit' });

export const metadata: Metadata = {
  title: 'Sadələşdirilmiş Vergi Kalkulyatoru',
  description: 'Azərbaycan Vergi Məcəlləsinə əsasən sadələşdirilmiş vergi öhdəliyinizi hesablayın',
  keywords: ['Azərbaycan', 'vergi', 'sadələşdirilmiş vergi', 'kalkulyator', 'hesablama', 'biznes'],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const t = dictionary.layout;

  return (
    <html lang="az">
      <body className={`${inter.variable} ${outfit.variable} font-sans antialiased bg-slate-50 selection:bg-primary-200 selection:text-primary-900`}>
        <div className="min-h-screen flex flex-col">
          <header className="fixed top-0 left-0 right-0 z-50 transition-all duration-300">
            <div className="absolute inset-0 glass border-b border-white/20 shadow-sm" />
            <div className="relative mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 h-16 sm:h-20 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 sm:h-11 sm:w-11 items-center justify-center rounded-xl bg-gradient-to-br from-primary-600 to-primary-700 text-white shadow-lg shadow-primary-500/30 ring-1 ring-white/20">
                  <Scale className="w-5 h-5 sm:w-6 sm:h-6" />
                </div>
                <div>
                  <h1 className="text-base sm:text-lg font-bold text-slate-900 font-heading leading-tight tracking-tight">
                    {t.header.title}
                  </h1>
                  <p className="text-[10px] sm:text-xs text-slate-500 font-medium tracking-wide uppercase">
                    {t.header.subtitle}
                  </p>
                </div>
              </div>

              <div className="hidden sm:flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100/50 border border-slate-200/50 backdrop-blur-sm">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-success-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-success-500"></span>
                </span>
                <span className="text-xs font-semibold text-slate-600 tracking-wide uppercase">{dictionary.common.pilotVersion}</span>
              </div>
            </div>
          </header>

          <main className="flex-grow pt-24 sm:pt-28 pb-12 px-4 sm:px-6">
            <div className="mx-auto max-w-6xl">
              {children}
            </div>
          </main>

          <footer className="mt-auto border-t border-slate-200 bg-white/50 backdrop-blur-sm">
            <div className="mx-auto max-w-6xl px-4 py-8 md:py-12">
              <div className="flex flex-col md:flex-row justify-between items-center gap-6 text-sm text-slate-500">
                <div className="flex flex-col items-center md:items-start gap-2">
                  <p className="font-medium text-slate-900">{dictionary.common.basedOn}</p>
                  <a
                    href="https://taxes.gov.az/az/page/vergi-mecellesi"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-1.5 text-primary-600 hover:text-primary-700 hover:underline transition-colors group"
                  >
                    <span>{dictionary.common.taxCode}</span>
                    <svg className="w-4 h-4 transform group-hover:translate-x-0.5 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </a>
                </div>
                <div className="text-center md:text-right">
                  <p className="mb-1">© {new Date().getFullYear()} {t.footer.rights}</p>
                  <p className="text-xs text-slate-400 max-w-md">
                    {dictionary.common.consulProfessional}
                  </p>
                </div>
              </div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
