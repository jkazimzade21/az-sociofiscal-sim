'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { dictionary } from '@/lib/dictionary';

const data = [
    { name: 'Sadələşdirilmiş (Bakı)', rate: 2, color: '#0ea5e9' },
    { name: 'Əvvəlki (Bakı)', rate: 4, color: '#94a3b8' },
    { name: 'Regionlar', rate: 2, color: '#10b981' },
];

export default function TaxChart() {
    return (
        <div className="w-full bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
            <div className="mb-6">
                <h3 className="text-lg font-bold text-slate-900 font-heading">Vergi Dərəcələrinin Müqayisəsi</h3>
                <p className="text-sm text-slate-500">Sadələşdirilmiş vergi dərəcələrinin vizual müqayisəsi (%)</p>
            </div>

            <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                        <XAxis
                            dataKey="name"
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: '#64748b', fontSize: 12 }}
                            dy={10}
                        />
                        <YAxis
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: '#64748b', fontSize: 12 }}
                            unit="%"
                        />
                        <Tooltip
                            cursor={{ fill: '#f8fafc' }}
                            contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                        />
                        <Bar dataKey="rate" radius={[6, 6, 0, 0]}>
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
