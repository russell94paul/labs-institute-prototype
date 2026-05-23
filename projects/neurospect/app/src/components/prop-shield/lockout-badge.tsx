import { cn } from '@/lib/utils';
import { LOCKOUT_STATE_LABELS, LOCKOUT_STATE_STYLES } from '@/lib/constants';
import type { LockoutState } from '@/types/api';

interface Props {
  state: LockoutState;
  className?: string;
}

export function LockoutBadge({ state, className }: Props) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium',
        LOCKOUT_STATE_STYLES[state],
        className,
      )}
    >
      {LOCKOUT_STATE_LABELS[state]}
    </span>
  );
}
