'use client';

import Hero from '@/components/ui/Hero';
import FeatureGrid from '@/components/ui/FeatureGrid';
import TaxChart from '@/components/analytics/TaxChart';

export default function Home() {
  return (
    <div className="space-y-20 pb-20">
      {/* Hero Section */}
      <section>
        <Hero />
      </section>

      {/* Features Section */}
      <section className="relative">
        <div className="absolute inset-0 bg-slate-50 skew-y-3 transform -z-10" />
        <div className="py-12">
          <FeatureGrid />
        </div>
      </section>

      {/* Visualizations Section */}
      <section className="max-w-4xl mx-auto px-4">
        <div className="grid md:grid-cols-2 gap-8 items-center">
          <div className="space-y-6">
            <h2 className="text-3xl font-bold text-slate-900 font-heading">
              Vergi yükünüzü <span className="text-primary-600">optimallaşdırın</span>
            </h2>
            <p className="text-lg text-slate-600 leading-relaxed">
              Sadələşdirilmiş vergi rejimi kiçik sahibkarlar üçün ən optimal həll yoludur.
              Bakı şəhərində və regionlarda tətbiq edilən güzəştli dərəcələrlə tanış olun.
            </p>
            <div className="flex flex-col gap-3">
              <div className="flex items-center gap-3 text-slate-700">
                <span className="w-2 h-2 rounded-full bg-primary-500" />
                <span>Bakı şəhəri üzrə: <strong>2%</strong></span>
              </div>
              <div className="flex items-center gap-3 text-slate-700">
                <span className="w-2 h-2 rounded-full bg-success-500" />
                <span>Regionlar üzrə: <strong>2%</strong></span>
              </div>
            </div>
          </div>

          <div className="w-full">
            <TaxChart />
          </div>
        </div>
      </section>
    </div>
  );
}
