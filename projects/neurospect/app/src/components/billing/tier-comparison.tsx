import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Check } from 'lucide-react';
import { cn } from '@/lib/utils';
import { UpgradeButton } from './upgrade-button';
import type { BillingTier } from '@/types/api';

interface TierDef {
  tier: BillingTier;
  name: string;
  price: string;
  features: string[];
}

const TIERS: TierDef[] = [
  {
    tier: 'free',
    name: 'Free',
    price: '$0',
    features: ['Trade journal', 'Basic analytics', 'Tradovate sync'],
  },
  {
    tier: 'mentor',
    name: 'Mentor',
    price: '$29/mo',
    features: ['Everything in Free', 'AI Coach (real-time alerts)', 'TradingView integration', 'Trade review'],
  },
  {
    tier: 'trader',
    name: 'Trader',
    price: '$99/mo',
    features: ['Everything in Mentor', 'Prop Shield (all firms)', 'Advanced analytics', 'Priority support'],
  },
];

interface Props {
  currentTier: BillingTier;
}

export function TierComparison({ currentTier }: Props) {
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
      {TIERS.map((t) => {
        const isCurrent = t.tier === currentTier;
        return (
          <Card key={t.tier} className={cn(isCurrent && 'border-primary ring-1 ring-primary')}>
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center justify-between">
                <span>{t.name}</span>
                <span className="text-lg font-semibold">{t.price}</span>
              </CardTitle>
              {isCurrent && (
                <p className="text-xs font-medium text-primary">Current plan</p>
              )}
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {t.features.map((f) => (
                  <li key={f} className="flex items-start gap-2 text-sm">
                    <Check className="mt-0.5 h-4 w-4 shrink-0 text-green-600" />
                    <span>{f}</span>
                  </li>
                ))}
              </ul>
              {!isCurrent && t.tier !== 'free' && (
                <div className="mt-4">
                  <UpgradeButton tier={t.tier} />
                </div>
              )}
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
