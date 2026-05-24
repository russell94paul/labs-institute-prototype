import { Link } from 'react-router-dom';
import { format } from 'date-fns';
import { AlertTriangle, TrendingUp } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { SummaryCards } from '@/components/analytics/summary-cards';
import { BreakdownTable } from '@/components/analytics/breakdown-table';
import { DayOfWeekChart } from '@/components/analytics/day-of-week-chart';
import { MistakeChart } from '@/components/analytics/mistake-chart';
import { RDistribution } from '@/components/analytics/r-distribution';
import { useBySetup, useBySession, useByInstrument, useSummary, useBehaviorMetrics } from '@/hooks/use-analytics';
import { SETUP_TYPE_LABELS, SESSION_LABELS } from '@/lib/constants';
import { cn } from '@/lib/utils';

function TodayBehaviorBanner() {
  const today = format(new Date(), 'yyyy-MM-dd');
  const { data } = useBehaviorMetrics(today, today);

  if (!data || data.trade_count === 0) return null;

  const alerts: string[] = [];
  if (data.tilt.score >= 60) alerts.push(`Tilt ${data.tilt.score}/100`);
  if (data.tilt.consecutive_losses >= 3) alerts.push(`${data.tilt.consecutive_losses} consecutive losses`);
  if (data.revenge_trades.length > 0) alerts.push(`${data.revenge_trades.length} revenge trade(s)`);
  if (data.overtrading.overtrading_days > 0) alerts.push('Overtrading today');

  if (alerts.length === 0) {
    return (
      <div className="flex items-center gap-2 rounded-lg border border-green-300 bg-green-50 px-4 py-2.5 text-sm text-green-800 dark:border-green-800 dark:bg-green-950/30 dark:text-green-300">
        <TrendingUp className="h-4 w-4 shrink-0" />
        <span>
          Clean session so far — {data.trade_count} trade(s), discipline {data.discipline.score}/100
        </span>
      </div>
    );
  }

  return (
    <div className={cn(
      'flex items-start gap-2 rounded-lg border px-4 py-2.5 text-sm',
      'border-amber-300 bg-amber-50 text-amber-900 dark:border-amber-800 dark:bg-amber-950/30 dark:text-amber-300'
    )}>
      <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
      <div>
        <span className="font-medium">Behavior alerts today: </span>
        {alerts.join(' · ')}
        <Link to="/analytics" className="ml-2 underline underline-offset-2 text-xs">
          View details
        </Link>
      </div>
    </div>
  );
}

function scoreColor(score: number, invert = false): string {
  const effective = invert ? 100 - score : score;
  if (effective >= 75) return 'text-green-600 dark:text-green-400';
  if (effective >= 50) return 'text-amber-500';
  return 'text-red-500';
}

function TodayScoreCards() {
  const today = format(new Date(), 'yyyy-MM-dd');
  const { data } = useBehaviorMetrics(today, today);

  if (!data || data.trade_count === 0) return null;

  const ruleAdherence = Math.round((1 - data.rule_breaches.rate) * 100);

  const metrics = [
    { label: 'Discipline', value: data.discipline.score, invert: false },
    { label: 'Consistency', value: data.consistency.score, invert: false },
    { label: 'Tilt Level', value: data.tilt.score, invert: true },
    { label: 'Rule Adherence', value: ruleAdherence, invert: false },
  ];

  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
      {metrics.map((m) => (
        <Card key={m.label} className="py-3">
          <CardHeader className="pb-1 pt-0 px-4">
            <CardTitle className="text-xs font-medium text-muted-foreground">{m.label} · Today</CardTitle>
          </CardHeader>
          <CardContent className="pb-0 px-4">
            <span className={cn('text-2xl font-semibold tabular-nums', scoreColor(m.value, m.invert))}>
              {m.value}
            </span>
            <span className="ml-0.5 text-xs text-muted-foreground">/100</span>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

export function DashboardPage() {
  const summary = useSummary();
  const bySetup = useBySetup();
  const bySession = useBySession();
  const byInstrument = useByInstrument();

  const hasNoTrades =
    !summary.isLoading && summary.data != null && summary.data.total_trades === 0;

  if (hasNoTrades) {
    return (
      <div className="flex flex-col items-center justify-center gap-4 py-24">
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <p className="max-w-sm text-center text-muted-foreground">
          Start journaling to see your analytics
        </p>
        <Button asChild>
          <Link to="/trades/new">Log Your First Trade</Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <Button variant="outline" size="sm" asChild>
          <Link to="/analytics">Full Analytics</Link>
        </Button>
      </div>

      <TodayBehaviorBanner />

      <TodayScoreCards />

      <SummaryCards />

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <BreakdownTable
          title="By Setup Type"
          rows={bySetup.data ?? []}
          labelMap={SETUP_TYPE_LABELS as Record<string, string>}
        />
        <BreakdownTable
          title="By Session"
          rows={bySession.data ?? []}
          labelMap={SESSION_LABELS as Record<string, string>}
        />
        <BreakdownTable title="By Instrument" rows={byInstrument.data ?? []} />
        <DayOfWeekChart />
        <MistakeChart />
        <RDistribution />
      </div>
    </div>
  );
}
