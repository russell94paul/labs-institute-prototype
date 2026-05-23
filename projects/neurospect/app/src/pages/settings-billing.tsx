import { useSearchParams } from 'react-router-dom';
import { SettingsShell } from '@/components/settings/settings-shell';
import { Skeleton } from '@/components/ui/skeleton';
import { Separator } from '@/components/ui/separator';
import { useSubscription } from '@/hooks/use-billing';
import { SubscriptionCard } from '@/components/billing/subscription-card';
import { TierComparison } from '@/components/billing/tier-comparison';

export function BillingSettingsPage() {
  const [searchParams] = useSearchParams();
  const justUpgraded = searchParams.get('success') === 'true';
  const { data: subscription, isLoading } = useSubscription();

  return (
    <SettingsShell>
      <div className="space-y-6 max-w-xl">
        <div>
          <h1 className="text-2xl font-semibold">Billing</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Manage your subscription and billing details.
          </p>
        </div>

        {justUpgraded && (
          <div className="rounded-md bg-green-50 p-3 text-sm text-green-800 dark:bg-green-900/20 dark:text-green-300">
            Subscription activated! Your new plan is now active.
          </div>
        )}

        <Separator />

        {isLoading ? (
          <div className="space-y-4">
            <Skeleton className="h-24 w-full rounded-lg" />
            <Skeleton className="h-64 w-full rounded-lg" />
          </div>
        ) : subscription ? (
          <>
            <section className="space-y-4">
              <SubscriptionCard subscription={subscription} />
            </section>

            <Separator />

            <section className="space-y-4">
              <h2 className="text-base font-medium">Available Plans</h2>
              <TierComparison currentTier={subscription.tier} />
            </section>
          </>
        ) : (
          <p className="text-sm text-muted-foreground">
            Unable to load subscription information.
          </p>
        )}
      </div>
    </SettingsShell>
  );
}
