'use client';

import { dictionary } from '@/lib/dictionary';
import { CheckCircle2, TrendingUp, BookOpen } from 'lucide-react';

export default function FeatureGrid() {
    const t = dictionary.home.features;

    const features = [
        {
            icon: <CheckCircle2 className="w-6 h-6 text-success-500" />,
            title: t.eligibility.title,
            desc: t.eligibility.desc,
            bg: "bg-success-50",
            border: "border-success-100"
        },
        {
            icon: <TrendingUp className="w-6 h-6 text-primary-500" />,
            title: t.calculation.title,
            desc: t.calculation.desc,
            bg: "bg-primary-50",
            border: "border-primary-100"
        },
        {
            icon: <BookOpen className="w-6 h-6 text-slate-500" />,
            title: t.legal.title,
            desc: t.legal.desc,
            bg: "bg-slate-50",
            border: "border-slate-200"
        }
    ];

    return (
        <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto px-4">
            {features.map((feature, idx) => (
                <div
                    key={idx}
                    className={`relative overflow-hidden p-6 rounded-2xl border ${feature.border} bg-white hover:shadow-lg transition-shadow duration-300 group`}
                >
                    <div className={`absolute top-0 right-0 w-24 h-24 -mr-8 -mt-8 rounded-full ${feature.bg} opacity-50 group-hover:scale-150 transition-transform duration-500`} />

                    <div className="relative z-10">
                        <div className={`w-12 h-12 rounded-xl ${feature.bg} flex items-center justify-center mb-4`}>
                            {feature.icon}
                        </div>
                        <h3 className="text-lg font-bold text-slate-900 mb-2 font-heading">
                            {feature.title}
                        </h3>
                        <p className="text-slate-600 text-sm leading-relaxed">
                            {feature.desc}
                        </p>
                    </div>
                </div>
            ))}
        </div>
    );
}
