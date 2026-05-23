import { Link, useParams } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Separator } from '@/components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { usePropConfig, usePropStatus } from '@/hooks/use-prop-shield';
import { LockoutBadge } from '@/components/prop-shield/lockout-badge';
import { RuleGaugeGrid } from '@/components/prop-shield/rule-gauge-grid';
import { ResetLockoutDialog } from '@/components/prop-shield/reset-lockout-dialog';
import { DeleteConfigDialog } from '@/components/prop-shield/delete-config-dialog';
import { LockoutHistoryTable } from '@/components/prop-shield/lockout-history-table';
import { DiscordWebhookSection } from '@/components/prop-shield/discord-webhook-section';
import { ConfigForm } from '@/components/prop-shield/config-form';
import { ACCOUNT_TYPE_LABELS } from '@/lib/constants';
import type { AccountType } from '@/types/api';

export function PropShieldDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data: config, isLoading: configLoading } = usePropConfig(id);
  const { data: status, isLoading: statusLoading } = usePropStatus(id);

  if (configLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-48" />
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-24 rounded-lg" />
          ))}
        </div>
      </div>
    );
  }

  if (!config) {
    return (
      <div className="flex flex-col items-center justify-center gap-4 py-24">
        <p className="text-muted-foreground">Account configuration not found.</p>
        <Button asChild variant="outline">
          <Link to="/prop-shield">Back to Prop Shield</Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="icon" asChild>
            <Link to="/prop-shield">
              <ArrowLeft className="h-4 w-4" />
            </Link>
          </Button>
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-semibold">{config.account_label}</h1>
              <LockoutBadge state={config.current_lockout_state} />
            </div>
            <p className="text-sm text-muted-foreground">
              {ACCOUNT_TYPE_LABELS[config.account_type as AccountType] ?? config.account_type} ·
              ${config.account_balance.toLocaleString()}
            </p>
          </div>
        </div>
        <DeleteConfigDialog configId={config.id} accountLabel={config.account_label} />
      </div>

      <Tabs defaultValue="status">
        <TabsList>
          <TabsTrigger value="status">Status</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        <TabsContent value="status" className="space-y-6 pt-4">
          {/* Rule Gauges */}
          {statusLoading ? (
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {Array.from({ length: 4 }).map((_, i) => (
                <Skeleton key={i} className="h-24 rounded-lg" />
              ))}
            </div>
          ) : status ? (
            <RuleGaugeGrid rules={status.rules} />
          ) : null}

          {/* Lockout Controls */}
          <div className="flex items-center gap-3">
            <ResetLockoutDialog
              configId={config.id}
              currentState={config.current_lockout_state}
            />
          </div>

          <Separator />

          {/* Lockout History */}
          <LockoutHistoryTable configId={config.id} />

          {/* Disclaimer */}
          {status?.disclaimer && (
            <p className="text-xs italic text-muted-foreground">{status.disclaimer}</p>
          )}
        </TabsContent>

        <TabsContent value="settings" className="space-y-6 pt-4">
          {/* Discord Webhook */}
          <DiscordWebhookSection
            configId={config.id}
            currentUrl={config.discord_webhook_url}
          />

          <Separator />

          {/* Edit Config Form */}
          <ConfigForm config={config} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
