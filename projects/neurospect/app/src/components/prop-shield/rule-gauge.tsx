import { Progress } from '@/components/ui/progress';
import { Card, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { RULE_LABELS } from '@/lib/constants';
import type { RuleBreachStatus } from '@/types/api';

interface Props {
  rule: RuleBreachStatus;
}

function gaugeColor(pct: number | null): string {
  if (pct == null) return '';
  if (pct >= 100) return '[&>div]:bg-red-500';
  if (pct >= 80) return '[&>div]:bg-orange-500';
  if (pct >= 60) return '[&>div]:bg-amber-500';
  return '[&>div]:bg-green-500';
}

function formatValue(value: number | null): string {
  if (value == null) return '—';
  return Number.isInteger(value) ? String(value) : value.toFixed(2);
}

export function RuleGauge({ rule }: Props) {
  if (!rule.active) return null;

  const pct = rule.pct_used ?? 0;
  const clampedPct = Math.min(pct, 100);
  const label = RULE_LABELS[rule.rule] ?? rule.rule;

  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium">{label}</span>
          <span className={cn('text-sm font-semibold', pct >= 100 ? 'text-red-600' : pct >= 80 ? 'text-orange-600' : 'text-muted-foreground')}>
            {pct.toFixed(0)}%
          </span>
        </div>
        <Progress value={clampedPct} className={cn('h-2', gaugeColor(pct))} />
        <div className="mt-2 flex justify-between text-xs text-muted-foreground">
          <span>{formatValue(rule.current_value)} / {formatValue(rule.limit)}</span>
          {rule.distance_to_breach != null && !rule.breached && (
            <span>{formatValue(rule.distance_to_breach)} remaining</span>
          )}
          {rule.breached && <span className="font-medium text-red-600">Breached</span>}
        </div>
      </CardContent>
    </Card>
  );
}
