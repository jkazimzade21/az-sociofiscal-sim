'use client';

import { motion } from 'framer-motion';
import { dictionary } from '@/lib/dictionary';
import Link from 'next/link';
import { ArrowRight, Calculator } from 'lucide-react';

export default function Hero() {
    const t = dictionary.home.hero;

    return (
        <div className="relative py-20 lg:py-32 overflow-hidden">
            {/* Background Glow */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-primary-200/30 rounded-full blur-[100px] animate-pulse-slow" />

            <div className="relative z-10 text-center max-w-4xl mx-auto space-y-8">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white border border-primary-200 text-primary-700 text-sm font-medium shadow-sm mb-4"
                >
                    <Calculator className="w-4 h-4" />
                    <span>{dictionary.common.pilotVersion}</span>
                </motion.div>

                <motion.h1
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.1 }}
                    className="text-4xl md:text-6xl lg:text-7xl font-bold font-heading tracking-tight"
                >
                    <span className="block text-slate-900 mb-2">Sadələşdirilmiş Vergi</span>
                    <span className="text-gradient">Asan Kalkulyator</span>
                </motion.h1>

                <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.2 }}
                    className="text-lg md:text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed"
                >
                    {t.subtitle}
                </motion.p>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.3 }}
                    className="flex flex-col sm:flex-row items-center justify-center gap-4"
                >
                    <Link href="/calculator" className="btn-primary text-lg px-8 py-4 w-full sm:w-auto group">
                        {t.cta}
                        <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                    </Link>
                    <p className="text-sm text-slate-500 mt-4 sm:mt-0">
                        {t.note}
                    </p>
                </motion.div>
            </div>
        </div>
    );
}
