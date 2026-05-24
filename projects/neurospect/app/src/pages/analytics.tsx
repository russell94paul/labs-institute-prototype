import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { BehaviorPanel } from '@/components/analytics/behavior-panel';
import { DrawdownChart } from '@/components/analytics/drawdown-chart';
import { EquityCurve } from '@/components/analytics/equity-curve';
import { MonthlyHeatmap } from '@/components/analytics/monthly-heatmap';
import { useCurrentMonthReport, useCurrentWeekReport, useRefreshThisMonth, useRefreshThisWeek } from '@/hooks/use-reports';
import { cn } from '@/lib/utils';
import type { UserReportResponse } from '@/types/api';

function statColor(value: number | null, low = 0.4, high = 0.6): string {
  if (value == null) return 'text-muted-foreground';
  if (value >= high) return 'text-green-600 dark:text-green-400';
  if (value >= low) return 'text-amber-500';
  return 'text-red-500';
}

function scoreColor(score: number, invert = false): string {
  const effective = invert ? 100 - score : score;
  if (effective >= 75) return 'text-green-600 dark:text-green-400';
  if (effective >= 50) return 'text-amber-500';
  return 'text-red-500';
}

function ReportCard({ report, label, onRefresh, isRefreshing }: {
  report: UserReportResponse | undefined;
  label: string;
  onRefresh: () => void;
  isRefreshing: boolean;
}) {
  if (!report) return <Skeleton className="h-48 w-full rounded-lg" />;

  const s = report.stats;

  const rows = [
    { label: 'Trades', value: String(s.trade_count) },
    { label: 'Win Rate', value: s.win_rate != null ? `${(s.win_rate * 100).toFixed(1)}%` : '—', colorClass: statColor(s.win_rate) },
    { label: 'Avg R', value: s.avg_r_multiple != null ? `${s.avg_r_multiple.toFixed(2)}R` : '—' },
    { label: 'Total R', value: `${s.total_r >= 0 ? '+' : ''}${s.total_r.toFixed(2)}R`, colorClass: s.total_r >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-500' },
    { label: 'Discipline', value: String(s.discipline_score), colorClass: scoreColor(s.discipline_score) },
    { label: 'Tilt Score', value: String(s.tilt_score), colorClass: scoreColor(s.tilt_score, true) },
    { label: 'Consistency', value: String(s.consistency_score), colorClass: scoreColor(s.consistency_score) },
    { label: 'Rule Breach %', value: `${(s.rule_breach_rate * 100).toFixed(0)}%`, colorClass: s.rule_breach_rate <= 0.1 ? 'text-green-600 dark:text-green-400' : s.rule_breach_rate <= 0.3 ? 'text-amber-500' : 'text-red-500' },
    { label: 'Revenge Trades', value: String(s.revenge_trade_count), colorClass: s.revenge_trade_count === 0 ? 'text-green-600 dark:text-green-400' : 'text-red-500' },
  ];

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-semibold">{label}</CardTitle>
        <Button
          variant="ghost"
          size="sm"
          className="h-7 text-xs"
          onClick={onRefresh}
          disabled={isRefreshing}
        >
          {isRefreshing ? 'Refreshing…' : 'Refresh'}
        </Button>
      </CardHeader>
      <CardContent>
        <dl className="grid grid-cols-3 gap-x-4 gap-y-3">
          {rows.map(({ label, value, colorClass }) => (
            <div key={label}>
              <dt className="text-[11px] text-muted-foreground">{label}</dt>
              <dd className={cn('text-sm font-semibold tabular-nums', colorClass)}>{value}</dd>
            </div>
          ))}
        </dl>
        <p className="mt-3 text-[10px] text-muted-foreground">
          Computed {new Date(report.computed_at).toLocaleString()}
        </p>
      </CardContent>
    </Card>
  );
}

function ReportsPanel() {
  const weekReport = useCurrentWeekReport();
  const monthReport = useCurrentMonthReport();
  const refreshWeek = useRefreshThisWeek();
  const refreshMonth = useRefreshThisMonth();

  return (
    <div className="space-y-4">
      <p className="text-xs text-muted-foreground">
        Reports are computed on demand and cached. Hit Refresh to recompute with latest trades.
      </p>
      <div className="grid gap-4 lg:grid-cols-2">
        <ReportCard
          report={weekReport.data}
          label="This Week"
          onRefresh={() => refreshWeek.mutate()}
          isRefreshing={refreshWeek.isPending}
        />
        <ReportCard
          report={monthReport.data}
          label="This Month"
          onRefresh={() => refreshMonth.mutate()}
          isRefreshing={refreshMonth.isPending}
        />
      </div>
    </div>
  );
}

export function AnalyticsPage() {
  const [dateStart, setDateStart] = useState('');
  const [dateEnd, setDateEnd] = useState('');

  const ds = dateStart || undefined;
  const de = dateEnd || undefined;

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <h1 className="text-2xl font-semibold">Analytics</h1>
        <div className="flex items-end gap-3">
          <div className="space-y-1">
            <Label className="text-xs text-muted-foreground">From</Label>
            <Input
              type="date"
              value={dateStart}
              onChange={(e) => setDateStart(e.target.value)}
              className="h-8 text-xs"
            />
          </div>
          <div className="space-y-1">
            <Label className="text-xs text-muted-foreground">To</Label>
            <Input
              type="date"
              value={dateEnd}
              onChange={(e) => setDateEnd(e.target.value)}
              className="h-8 text-xs"
            />
          </div>
        </div>
      </div>

      <Tabs defaultValue="behavior">
        <TabsList>
          <TabsTrigger value="behavior">Behavior</TabsTrigger>
          <TabsTrigger value="equity">Equity Curve</TabsTrigger>
          <TabsTrigger value="drawdown">Drawdown</TabsTrigger>
          <TabsTrigger value="heatmap">Monthly Heatmap</TabsTrigger>
          <TabsTrigger value="reports">Reports</TabsTrigger>
        </TabsList>

        <TabsContent value="behavior" className="mt-4">
          <BehaviorPanel dateStart={ds} dateEnd={de} />
        </TabsContent>

        <TabsContent value="equity" className="mt-4">
          <EquityCurve dateStart={ds} dateEnd={de} />
        </TabsContent>

        <TabsContent value="drawdown" className="mt-4">
          <DrawdownChart dateStart={ds} dateEnd={de} />
        </TabsContent>

        <TabsContent value="heatmap" className="mt-4">
          <MonthlyHeatmap dateStart={ds} dateEnd={de} />
        </TabsContent>

        <TabsContent value="reports" className="mt-4">
          <ReportsPanel />
        </TabsContent>
      </Tabs>
    </div>
  );
}
