import { Card, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { usePresets } from '@/hooks/use-prop-shield';
import { Settings2 } from 'lucide-react';
import type { PropFirmPreset } from '@/types/api';

interface Props {
  onSelect: (preset: PropFirmPreset | null) => void;
}

export function PresetPicker({ onSelect }: Props) {
  const { data: presets, isLoading } = usePresets();

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-28 rounded-lg" />
        ))}
      </div>
    );
  }

  const grouped = new Map<string, PropFirmPreset[]>();
  for (const p of presets ?? []) {
    const list = grouped.get(p.firm_name) ?? [];
    list.push(p);
    grouped.set(p.firm_name, list);
  }

  return (
    <div className="space-y-6">
      {Array.from(grouped.entries()).map(([firm, firmPresets]) => (
        <div key={firm}>
          <h3 className="mb-2 text-sm font-semibold text-muted-foreground">{firm}</h3>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {firmPresets.map((p) => (
              <Card
                key={p.preset_id}
                className="cursor-pointer transition-shadow hover:shadow-md"
                onClick={() => onSelect(p)}
              >
                <CardContent className="p-4">
                  <p className="font-medium">{p.account_size}</p>
                  <div className="mt-1 flex flex-wrap gap-x-3 gap-y-1 text-xs text-muted-foreground">
                    {p.daily_loss_limit != null && <span>Daily: ${p.daily_loss_limit.toLocaleString()}</span>}
                    {p.trailing_drawdown_limit != null && <span>DD: ${p.trailing_drawdown_limit.toLocaleString()}</span>}
                    {p.max_contracts != null && <span>Max: {p.max_contracts} contracts</span>}
                  </div>
                  {p.notes && <p className="mt-2 text-xs text-muted-foreground italic">{p.notes}</p>}
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      ))}

      <div>
        <h3 className="mb-2 text-sm font-semibold text-muted-foreground">Other</h3>
        <Card
          className="cursor-pointer transition-shadow hover:shadow-md"
          onClick={() => onSelect(null)}
        >
          <CardContent className="flex items-center gap-3 p-4">
            <Settings2 className="h-5 w-5 text-muted-foreground" />
            <div>
              <p className="font-medium">Custom Configuration</p>
              <p className="text-xs text-muted-foreground">Set up rules manually</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
