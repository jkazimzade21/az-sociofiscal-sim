/**
 * Utility functions for the frontend.
 */

import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Merge Tailwind CSS classes with clsx.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Format currency in AZN.
 */
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('az-AZ', {
    style: 'currency',
    currency: 'AZN',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
}

/**
 * Format percentage.
 */
export function formatPercent(value: number): string {
  return new Intl.NumberFormat('az-AZ', {
    style: 'percent',
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(value);
}

/**
 * Get readable route name.
 */
export function getRouteName(route: string): string {
  const routeNames: Record<string, string> = {
    general: 'General Simplified Tax',
    trade_catering_over_200k: 'Trade/Catering (>200k)',
    auto_transport: 'Passenger Transport/Taxi',
    auto_betting_lottery: 'Betting/Lottery',
    auto_property: 'Property Transfer',
    auto_land: 'Land Transfer',
    auto_fixed_220_10: 'Fixed Activity (220.10)',
  };
  return routeNames[route] || route;
}

/**
 * Get location zone display name.
 */
export function getZoneName(zone: string): string {
  const zoneNames: Record<string, string> = {
    baku_center: 'Baku Center (Zone 1)',
    baku_other: 'Baku Other Areas (Zone 2)',
    sumgait_ganja_lankaran: 'Sumgait/Ganja/Lankaran',
    other_cities: 'Other Cities',
    rural: 'Rural Areas',
  };
  return zoneNames[zone] || zone;
}
