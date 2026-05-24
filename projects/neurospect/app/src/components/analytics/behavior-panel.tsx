import { AlertTriangle, CheckCircle2, TrendingDown } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { useBehaviorMetrics } from '@/hooks/use-analytics';
import { cn } from '@/lib/utils';

function ScorePill({ score, invert = false }: { score: number; invert?: boolean }) {
  // invert=true means high score is bad (e.g. tilt)
  const effective = invert ? 100 - score : score;
  const color =
    effective >= 75 ? 'text-green-600' :
    effective >= 50 ? 'text-amber-500' :
    'text-red-500';
  return <span className={cn('text-2xl font-semibold tabular-nums', color)}>{score}</span>;
}

function Alert({ message, type }: { message: string; type: 'warn' | 'ok' }) {
  return (
    <div className={cn(
      'flex items-start gap-2 rounded-md border px-3 py-2 text-xs',
      type === 'warn'
        ? 'border-amber-300 bg-amber-50 text-amber-800 dark:border-amber-800 dark:bg-amber-950/30 dark:text-amber-300'
        : 'border-green-300 bg-green-50 text-green-800 dark:border-green-800 dark:bg-green-950/30 dark:text-green-300'
    )}>
      {type === 'warn'
        ? <AlertTriangle className="mt-0.5 h-3.5 w-3.5 shrink-0" />
        : <CheckCircle2 className="mt-0.5 h-3.5 w-3.5 shrink-0" />}
      <span>{message}</span>
    </div>
  );
}

interface Props {
  dateStart?: string;
  dateEnd?: string;
}

export function BehaviorPanel({ dateStart, dateEnd }: Props) {
  const { data, isLoading } = useBehaviorMetrics(dateStart, dateEnd);

  if (isLoading) {
    return (
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-24 rounded-lg" />
        ))}
      </div>
    );
  }

  if (!data || data.trade_count === 0) {
    return (
      <div className="rounded-lg border p-6 text-center text-muted-foreground">
        <TrendingDown className="mx-auto mb-2 h-8 w-8 opacity-30" />
        <p className="text-sm">No trades in the selected period</p>
      </div>
    );
  }

  // Build alerts
  const alerts: { message: string; type: 'warn' | 'ok' }[] = [];

  if (data.tilt.score >= 60) {
    alerts.push({ message: `Tilt score ${data.tilt.score}/100 — consider stepping away`, type: 'warn' });
  }
  if (data.tilt.consecutive_losses >= 3) {
    alerts.push({ message: `${data.tilt.consecutive_losses} consecutive losses detected`, type: 'warn' });
  }
  if (data.revenge_trades.length > 0) {
    alerts.push({ message: `${data.revenge_trades.length} potential revenge trade(s) detected`, type: 'warn' });
  }
  if (data.overtrading.overtrading_days > 0) {
    alerts.push({ message: `Overtraded on ${data.overtrading.overtrading_days} day(s) this period`, type: 'warn' });
  }
  if (data.rule_breaches.rate > 0.3) {
    alerts.push({ message: `${(data.rule_breaches.rate * 100).toFixed(0)}% of trades had rule breaches`, type: 'warn' });
  }
  if (data.discipline.score >= 75 && alerts.length === 0) {
    alerts.push({ message: `Strong discipline this period (${data.discipline.score}/100)`, type: 'ok' });
  }

  const metrics = [
    { title: 'Discipline', score: data.discipline.score, invert: false },
    { title: 'Consistency', score: data.consistency.score, invert: false },
    { title: 'Tilt Level', score: data.tilt.score, invert: true },
    { title: 'Rule Adherence', score: Math.round((1 - data.rule_breaches.rate) * 100), invert: false },
  ];

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        {metrics.map((m) => (
          <Card key={m.title}>
            <CardHeader className="pb-1 pt-4">
              <CardTitle className="text-xs font-medium text-muted-foreground">{m.title}</CardTitle>
            </CardHeader>
            <CardContent className="pb-4">
              <ScorePill score={m.score} invert={m.invert} />
              <span className="ml-1 text-xs text-muted-foreground">/100</span>
            </CardContent>
          </Card>
        ))}
      </div>

      {alerts.length > 0 && (
        <div className="space-y-2">
          {alerts.map((a, i) => (
            <Alert key={i} message={a.message} type={a.type} />
          ))}
        </div>
      )}

      {data.tilt.consecutive_losses > 0 || data.tilt.rapid_reentries > 0 ? (
        <div className="grid grid-cols-3 gap-3 text-xs">
          <div className="rounded border p-3">
            <p className="text-muted-foreground">Consec. Losses</p>
            <p className="mt-1 text-lg font-semibold">{data.tilt.consecutive_losses}</p>
          </div>
          <div className="rounded border p-3">
            <p className="text-muted-foreground">Rapid Re-entries</p>
            <p className="mt-1 text-lg font-semibold">{data.tilt.rapid_reentries}</p>
          </div>
          <div className="rounded border p-3">
            <p className="text-muted-foreground">Position Escalations</p>
            <p className="mt-1 text-lg font-semibold">{data.tilt.position_escalations}</p>
          </div>
        </div>
      ) : null}
    </div>
  );
}
