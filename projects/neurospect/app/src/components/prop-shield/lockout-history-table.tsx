import { ChevronDown } from 'lucide-react';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { Skeleton } from '@/components/ui/skeleton';
import { Button } from '@/components/ui/button';
import { formatDate } from '@/lib/utils';
import { LOCKOUT_STATE_LABELS } from '@/lib/constants';
import { useLockoutHistory } from '@/hooks/use-prop-shield';
import type { LockoutState } from '@/types/api';

interface Props {
  configId: string;
}

export function LockoutHistoryTable({ configId }: Props) {
  const { data: events, isLoading } = useLockoutHistory(configId);

  return (
    <Collapsible>
      <CollapsibleTrigger asChild>
        <Button variant="ghost" size="sm" className="flex items-center gap-1">
          <ChevronDown className="h-4 w-4 transition-transform [[data-state=open]_&]:rotate-180" />
          Lockout History
          {events && <span className="text-muted-foreground">({events.length})</span>}
        </Button>
      </CollapsibleTrigger>
      <CollapsibleContent className="mt-2">
        {isLoading ? (
          <div className="space-y-2">
            {Array.from({ length: 3 }).map((_, i) => (
              <Skeleton key={i} className="h-10 w-full rounded" />
            ))}
          </div>
        ) : !events || events.length === 0 ? (
          <p className="text-sm text-muted-foreground">No lockout events recorded.</p>
        ) : (
          <div className="rounded-md border">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b bg-muted/50">
                  <th className="px-3 py-2 text-left font-medium">Date</th>
                  <th className="px-3 py-2 text-left font-medium">Transition</th>
                  <th className="px-3 py-2 text-left font-medium">Trigger</th>
                  <th className="px-3 py-2 text-left font-medium">Note</th>
                </tr>
              </thead>
              <tbody>
                {events.map((e) => (
                  <tr key={e.id} className="border-b last:border-0">
                    <td className="px-3 py-2 whitespace-nowrap">{formatDate(e.created_at)}</td>
                    <td className="px-3 py-2">
                      {LOCKOUT_STATE_LABELS[e.from_state as LockoutState]} {'→'} {LOCKOUT_STATE_LABELS[e.to_state as LockoutState]}
                    </td>
                    <td className="px-3 py-2">
                      {e.reset_by_user ? 'Manual reset' : e.trigger_rule ?? '—'}
                    </td>
                    <td className="px-3 py-2 text-muted-foreground">{e.note ?? '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </CollapsibleContent>
    </Collapsible>
  );
}
