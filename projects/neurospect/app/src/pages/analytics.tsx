import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { BehaviorPanel } from '@/components/analytics/behavior-panel';
import { DrawdownChart } from '@/components/analytics/drawdown-chart';
import { EquityCurve } from '@/components/analytics/equity-curve';
import { MonthlyHeatmap } from '@/components/analytics/monthly-heatmap';

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
      </Tabs>
    </div>
  );
}
