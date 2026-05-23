import { useNavigate } from 'react-router-dom';
import { Card, CardContent } from '@/components/ui/card';
import { LockoutBadge } from './lockout-badge';
import { ACCOUNT_TYPE_LABELS } from '@/lib/constants';
import type { PropRuleConfigResponse, AccountType } from '@/types/api';

interface Props {
  config: PropRuleConfigResponse;
}

export function ConfigCard({ config }: Props) {
  const navigate = useNavigate();

  return (
    <Card
      className="cursor-pointer transition-shadow hover:shadow-md"
      onClick={() => navigate(`/prop-shield/${config.id}`)}
    >
      <CardContent className="flex items-start justify-between gap-4 p-4">
        <div className="flex flex-col gap-1">
          <span className="font-semibold">{config.account_label}</span>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span>{ACCOUNT_TYPE_LABELS[config.account_type as AccountType] ?? config.account_type}</span>
            <span>&middot;</span>
            <span>${config.account_balance.toLocaleString()}</span>
          </div>
          <div className="mt-1 flex flex-wrap gap-3 text-xs text-muted-foreground">
            {config.daily_loss_limit != null && (
              <span>Daily: ${config.daily_loss_limit.toLocaleString()}</span>
            )}
            {config.trailing_drawdown_limit != null && (
              <span>DD: ${config.trailing_drawdown_limit.toLocaleString()}</span>
            )}
            {config.max_contracts != null && (
              <span>Max: {config.max_contracts} contracts</span>
            )}
          </div>
        </div>
        <LockoutBadge state={config.current_lockout_state} />
      </CardContent>
    </Card>
  );
}
