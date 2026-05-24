import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { useDrawdown } from '@/hooks/use-analytics';
import { Skeleton } from '@/components/ui/skeleton';

interface Props {
  dateStart?: string;
  dateEnd?: string;
}

export function DrawdownChart({ dateStart, dateEnd }: Props) {
  const { data, isLoading } = useDrawdown(dateStart, dateEnd);

  if (isLoading) return <Skeleton className="h-64 w-full rounded-lg" />;

  if (!data || data.points.length === 0) {
    return (
      <div className="flex h-64 items-center justify-center rounded-lg border">
        <p className="text-sm text-muted-foreground">No closed trades yet</p>
      </div>
    );
  }

  const chartData = data.points.map((p) => ({
    date: p.date.slice(5),
    dd: -p.drawdown_r,  // negate so the chart shows valleys going down
  }));

  return (
    <div className="rounded-lg border">
      <div className="border-b px-4 py-3 flex items-center justify-between">
        <h3 className="text-sm font-semibold">Drawdown</h3>
        <div className="flex gap-4 text-xs text-muted-foreground">
          <span>Max: <span className="font-medium text-red-500">{data.max_drawdown_r.toFixed(2)}R</span></span>
          <span>Current: <span className="font-medium">{data.current_drawdown_r.toFixed(2)}R</span></span>
        </div>
      </div>
      <div className="p-4">
        <ResponsiveContainer width="100%" height={220}>
          <AreaChart data={chartData} margin={{ top: 4, right: 16, left: 0, bottom: 4 }}>
            <defs>
              <linearGradient id="ddGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#ef4444" stopOpacity={0.05} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
            <XAxis
              dataKey="date"
              tick={{ fontSize: 11 }}
              tickLine={false}
              axisLine={false}
              interval="preserveStartEnd"
            />
            <YAxis
              tick={{ fontSize: 11 }}
              tickLine={false}
              axisLine={false}
              tickFormatter={(v) => `${Math.abs(v)}R`}
            />
            <Tooltip
              content={({ active, payload, label }) => {
                if (!active || !payload?.[0]) return null;
                const dd = Math.abs(payload[0].value as number);
                return (
                  <div className="rounded border bg-background p-2 text-xs shadow-md">
                    <p className="font-medium">{label}</p>
                    <p>Drawdown: {dd.toFixed(2)}R</p>
                  </div>
                );
              }}
            />
            <Area
              type="monotone"
              dataKey="dd"
              stroke="#ef4444"
              fill="url(#ddGrad)"
              strokeWidth={2}
              dot={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
