import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { useEquityCurve } from '@/hooks/use-analytics';
import { Skeleton } from '@/components/ui/skeleton';

interface Props {
  dateStart?: string;
  dateEnd?: string;
}

export function EquityCurve({ dateStart, dateEnd }: Props) {
  const { data, isLoading } = useEquityCurve(dateStart, dateEnd);

  if (isLoading) return <Skeleton className="h-64 w-full rounded-lg" />;

  if (!data || data.length === 0) {
    return (
      <div className="flex h-64 items-center justify-center rounded-lg border">
        <p className="text-sm text-muted-foreground">No closed trades yet</p>
      </div>
    );
  }

  const chartData = data.map((p) => ({
    date: p.date.slice(5),  // "MM-DD"
    r: p.cumulative_r,
    pnl: p.cumulative_pnl,
  }));

  const isPositive = chartData[chartData.length - 1].r >= 0;

  return (
    <div className="rounded-lg border">
      <div className="border-b px-4 py-3">
        <h3 className="text-sm font-semibold">Equity Curve (Cumulative R)</h3>
      </div>
      <div className="p-4">
        <ResponsiveContainer width="100%" height={220}>
          <LineChart data={chartData} margin={{ top: 4, right: 16, left: 0, bottom: 4 }}>
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
              tickFormatter={(v) => `${v}R`}
            />
            <Tooltip
              content={({ active, payload, label }) => {
                if (!active || !payload?.[0]) return null;
                const d = payload[0].payload;
                return (
                  <div className="rounded border bg-background p-2 text-xs shadow-md">
                    <p className="font-medium">{label}</p>
                    <p>Cumulative R: {d.r.toFixed(2)}R</p>
                    {d.pnl != null && <p>Cumulative PnL: ${d.pnl.toLocaleString()}</p>}
                  </div>
                );
              }}
            />
            <Line
              type="monotone"
              dataKey="r"
              stroke={isPositive ? '#22c55e' : '#ef4444'}
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
