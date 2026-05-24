import { useMonthlyHeatmap } from '@/hooks/use-analytics';
import { Skeleton } from '@/components/ui/skeleton';
import { cn } from '@/lib/utils';

const MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

function cellColor(totalR: number): string {
  if (totalR > 5) return 'bg-green-600 text-white';
  if (totalR > 2) return 'bg-green-400 text-white';
  if (totalR > 0) return 'bg-green-200 text-green-900';
  if (totalR === 0) return 'bg-muted text-muted-foreground';
  if (totalR > -2) return 'bg-red-200 text-red-900';
  if (totalR > -5) return 'bg-red-400 text-white';
  return 'bg-red-600 text-white';
}

interface Props {
  dateStart?: string;
  dateEnd?: string;
}

export function MonthlyHeatmap({ dateStart, dateEnd }: Props) {
  const { data, isLoading } = useMonthlyHeatmap(dateStart, dateEnd);

  if (isLoading) return <Skeleton className="h-48 w-full rounded-lg" />;

  if (!data || data.length === 0) {
    return (
      <div className="flex h-48 items-center justify-center rounded-lg border">
        <p className="text-sm text-muted-foreground">No closed trades yet</p>
      </div>
    );
  }

  // Group by year
  const byYear: Record<number, Record<number, (typeof data)[0]>> = {};
  for (const cell of data) {
    if (!byYear[cell.year]) byYear[cell.year] = {};
    byYear[cell.year][cell.month] = cell;
  }
  const years = Object.keys(byYear).map(Number).sort();

  return (
    <div className="rounded-lg border">
      <div className="border-b px-4 py-3">
        <h3 className="text-sm font-semibold">Monthly Heatmap (R)</h3>
      </div>
      <div className="p-4 space-y-4 overflow-x-auto">
        {years.map((year) => (
          <div key={year}>
            <p className="mb-2 text-xs font-medium text-muted-foreground">{year}</p>
            <div className="grid grid-cols-12 gap-1">
              {MONTH_NAMES.map((name, idx) => {
                const month = idx + 1;
                const cell = byYear[year]?.[month];
                return (
                  <div
                    key={month}
                    title={cell
                      ? `${name} ${year}: ${cell.total_r.toFixed(2)}R, ${cell.trade_count} trades`
                      : `${name} ${year}: no data`}
                    className={cn(
                      'flex flex-col items-center justify-center rounded p-1 text-center text-[10px] min-h-[48px]',
                      cell ? cellColor(cell.total_r) : 'bg-muted/40 text-muted-foreground'
                    )}
                  >
                    <span className="font-medium">{name}</span>
                    {cell && (
                      <span className="mt-0.5 font-bold">
                        {cell.total_r > 0 ? '+' : ''}{cell.total_r.toFixed(1)}R
                      </span>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
