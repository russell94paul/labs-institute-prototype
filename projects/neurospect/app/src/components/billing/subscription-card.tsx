import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { BILLING_TIER_LABELS, SUBSCRIPTION_STATUS_LABELS, SUBSCRIPTION_STATUS_STYLES } from '@/lib/constants';
import { formatDate } from '@/lib/utils';
import type { SubscriptionResponse } from '@/types/api';

interface Props {
  subscription: SubscriptionResponse;
}

export function SubscriptionCard({ subscription }: Props) {
  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">Current Plan</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex items-center gap-3">
          <p className="text-2xl font-semibold">{BILLING_TIER_LABELS[subscription.tier]}</p>
          <span
            className={cn(
              'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium',
              SUBSCRIPTION_STATUS_STYLES[subscription.status],
            )}
          >
            {SUBSCRIPTION_STATUS_LABELS[subscription.status]}
          </span>
        </div>
        {subscription.current_period_end && subscription.status === 'active' && (
          <p className="mt-1 text-sm text-muted-foreground">
            Renews {formatDate(subscription.current_period_end)}
          </p>
        )}
        {subscription.status === 'canceled' && subscription.current_period_end && (
          <p className="mt-1 text-sm text-muted-foreground">
            Access until {formatDate(subscription.current_period_end)}
          </p>
        )}
      </CardContent>
    </Card>
  );
}
