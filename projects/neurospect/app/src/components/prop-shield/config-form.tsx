import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Separator } from '@/components/ui/separator';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { useCreatePropConfig, useUpdatePropConfig } from '@/hooks/use-prop-shield';
import { ACCOUNT_TYPE_OPTIONS } from '@/lib/constants';
import type { PropRuleConfigResponse } from '@/types/api';

// ============================================================
// Schema
// ============================================================

const configFormSchema = z.object({
  account_label: z.string().min(1, 'Required').max(128),
  account_type: z.enum(['sim', 'eval', 'funded']),
  preset: z.string().nullable().optional(),
  account_balance: z.number().positive('Must be positive'),
  daily_loss_limit: z.number().nonnegative().nullable().optional(),
  trailing_drawdown_limit: z.number().nonnegative().nullable().optional(),
  max_contracts: z.number().int().positive().nullable().optional(),
  max_daily_trades: z.number().int().positive().nullable().optional(),
  forbidden_hours_start: z
    .string()
    .regex(/^\d{2}:\d{2}$/, 'HH:MM format')
    .nullable()
    .optional()
    .or(z.literal('')),
  forbidden_hours_end: z
    .string()
    .regex(/^\d{2}:\d{2}$/, 'HH:MM format')
    .nullable()
    .optional()
    .or(z.literal('')),
  consistency_rule_pct: z.number().min(0).max(100).nullable().optional(),
  alert_threshold_pct: z.number().min(1).max(100),
  discord_webhook_url: z
    .string()
    .url('Must be a valid URL')
    .nullable()
    .optional()
    .or(z.literal('')),
  lockout_enabled: z.boolean(),
});

type ConfigFormValues = z.infer<typeof configFormSchema>;

// ============================================================
// Helpers
// ============================================================

function toFormValues(config: PropRuleConfigResponse): ConfigFormValues {
  return {
    account_label: config.account_label,
    account_type: config.account_type as ConfigFormValues['account_type'],
    preset: config.preset,
    account_balance: config.account_balance,
    daily_loss_limit: config.daily_loss_limit,
    trailing_drawdown_limit: config.trailing_drawdown_limit,
    max_contracts: config.max_contracts,
    max_daily_trades: config.max_daily_trades,
    forbidden_hours_start: config.forbidden_hours_start ?? '',
    forbidden_hours_end: config.forbidden_hours_end ?? '',
    consistency_rule_pct: config.consistency_rule_pct,
    alert_threshold_pct: config.alert_threshold_pct,
    discord_webhook_url: config.discord_webhook_url ?? '',
    lockout_enabled: config.lockout_enabled,
  };
}

/** Convert empty strings to null for optional fields before submission. */
function cleanPayload(values: ConfigFormValues): Record<string, unknown> {
  const cleaned: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(values)) {
    if (value === '' || value === undefined) {
      cleaned[key] = null;
    } else {
      cleaned[key] = value;
    }
  }
  return cleaned;
}

function buildPatch(
  values: ConfigFormValues,
  dirtyFields: Partial<Record<keyof ConfigFormValues, boolean | unknown>>,
): Record<string, unknown> {
  const patch: Record<string, unknown> = {};
  for (const [key, dirty] of Object.entries(dirtyFields)) {
    if (dirty) {
      const v = values[key as keyof ConfigFormValues];
      patch[key] = v === '' || v === undefined ? null : v;
    }
  }
  return patch;
}

const DEFAULT_VALUES: ConfigFormValues = {
  account_label: '',
  account_type: 'eval',
  preset: null,
  account_balance: 0,
  daily_loss_limit: null,
  trailing_drawdown_limit: null,
  max_contracts: null,
  max_daily_trades: null,
  forbidden_hours_start: '',
  forbidden_hours_end: '',
  consistency_rule_pct: null,
  alert_threshold_pct: 80,
  discord_webhook_url: '',
  lockout_enabled: false,
};

// ============================================================
// Component
// ============================================================

interface Props {
  config?: PropRuleConfigResponse; // If provided, edit mode
  presetValues?: Partial<ConfigFormValues>; // Pre-fill from preset
  onSuccess?: () => void;
}

export function ConfigForm({ config, presetValues, onSuccess }: Props) {
  const isEdit = !!config;

  const form = useForm<ConfigFormValues>({
    resolver: zodResolver(configFormSchema),
    defaultValues: isEdit ? toFormValues(config) : { ...DEFAULT_VALUES, ...presetValues },
  });

  const createConfig = useCreatePropConfig();
  const updateConfig = useUpdatePropConfig(config?.id ?? '');

  // Apply preset values when they change (e.g., user picks a new preset)
  useEffect(() => {
    if (!isEdit && presetValues) {
      form.reset({ ...DEFAULT_VALUES, ...presetValues }, { keepDirtyValues: true });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [presetValues]);

  const onSubmit = (values: ConfigFormValues) => {
    if (!isEdit) {
      const payload = cleanPayload(values);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      createConfig.mutate(payload as any, { onSuccess: () => onSuccess?.() });
    } else {
      const patch = buildPatch(values, form.formState.dirtyFields);
      if (Object.keys(patch).length === 0) return;
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      updateConfig.mutate(patch as any, { onSuccess: () => onSuccess?.() });
    }
  };

  const isBusy = createConfig.isPending || updateConfig.isPending;

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="flex flex-col gap-6">
        {/* ---- Account Info ---- */}
        <div>
          <h3 className="mb-3 text-sm font-semibold text-muted-foreground">Account Info</h3>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <FormField
              control={form.control}
              name="account_label"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Account Label</FormLabel>
                  <FormControl>
                    <Input placeholder="e.g. Apex 50K Eval #2" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="account_type"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Account Type</FormLabel>
                  <Select onValueChange={field.onChange} value={field.value}>
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Select type" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {ACCOUNT_TYPE_OPTIONS.map((opt) => (
                        <SelectItem key={opt.value} value={opt.value}>
                          {opt.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="account_balance"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Account Balance ($)</FormLabel>
                  <FormControl>
                    <Input
                      type="number"
                      step="0.01"
                      placeholder="50000"
                      {...field}
                      value={field.value ?? ''}
                      onChange={(e) => field.onChange(e.target.value === '' ? 0 : parseFloat(e.target.value))}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>
        </div>

        <Separator />

        {/* ---- Rule Limits ---- */}
        <div>
          <h3 className="mb-3 text-sm font-semibold text-muted-foreground">Rule Limits</h3>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField
              control={form.control}
              name="daily_loss_limit"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Daily Loss Limit ($)</FormLabel>
                  <FormControl>
                    <Input
                      type="number"
                      step="0.01"
                      placeholder="Optional"
                      {...field}
                      value={field.value ?? ''}
                      onChange={(e) => field.onChange(e.target.value === '' ? null : parseFloat(e.target.value))}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="trailing_drawdown_limit"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Trailing Drawdown Limit ($)</FormLabel>
                  <FormControl>
                    <Input
                      type="number"
                      step="0.01"
                      placeholder="Optional"
                      {...field}
                      value={field.value ?? ''}
                      onChange={(e) => field.onChange(e.target.value === '' ? null : parseFloat(e.target.value))}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="max_contracts"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Max Contracts</FormLabel>
                  <FormControl>
                    <Input
                      type="number"
                      step="1"
                      placeholder="Optional"
                      {...field}
                      value={field.value ?? ''}
                      onChange={(e) => field.onChange(e.target.value === '' ? null : parseInt(e.target.value, 10))}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="max_daily_trades"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Max Daily Trades</FormLabel>
                  <FormControl>
                    <Input
                      type="number"
                      step="1"
                      placeholder="Optional"
                      {...field}
                      value={field.value ?? ''}
                      onChange={(e) => field.onChange(e.target.value === '' ? null : parseInt(e.target.value, 10))}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>
        </div>

        <Separator />

        {/* ---- Schedule ---- */}
        <div>
          <h3 className="mb-3 text-sm font-semibold text-muted-foreground">Schedule</h3>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField
              control={form.control}
              name="forbidden_hours_start"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Forbidden Hours Start</FormLabel>
                  <FormControl>
                    <Input
                      type="time"
                      {...field}
                      value={field.value ?? ''}
                      onChange={(e) => field.onChange(e.target.value)}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="forbidden_hours_end"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Forbidden Hours End</FormLabel>
                  <FormControl>
                    <Input
                      type="time"
                      {...field}
                      value={field.value ?? ''}
                      onChange={(e) => field.onChange(e.target.value)}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>
        </div>

        <Separator />

        {/* ---- Advanced ---- */}
        <div>
          <h3 className="mb-3 text-sm font-semibold text-muted-foreground">Advanced</h3>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField
              control={form.control}
              name="consistency_rule_pct"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Consistency Rule (%)</FormLabel>
                  <FormControl>
                    <Input
                      type="number"
                      min="0"
                      max="100"
                      step="1"
                      placeholder="Optional (0-100)"
                      {...field}
                      value={field.value ?? ''}
                      onChange={(e) => field.onChange(e.target.value === '' ? null : parseFloat(e.target.value))}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="alert_threshold_pct"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Alert Threshold (%)</FormLabel>
                  <FormControl>
                    <Input
                      type="number"
                      min="1"
                      max="100"
                      step="1"
                      placeholder="80"
                      {...field}
                      value={field.value ?? ''}
                      onChange={(e) => field.onChange(e.target.value === '' ? 80 : parseInt(e.target.value, 10))}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>
        </div>

        <Separator />

        {/* ---- Alerts ---- */}
        <div>
          <h3 className="mb-3 text-sm font-semibold text-muted-foreground">Alerts</h3>
          <div className="flex flex-col gap-4">
            <FormField
              control={form.control}
              name="discord_webhook_url"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Discord Webhook URL</FormLabel>
                  <FormControl>
                    <Input
                      type="url"
                      placeholder="https://discord.com/api/webhooks/..."
                      {...field}
                      value={field.value ?? ''}
                      onChange={(e) => field.onChange(e.target.value)}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="lockout_enabled"
              render={({ field }) => (
                <FormItem className="flex flex-row items-center gap-3 space-y-0">
                  <FormControl>
                    <Checkbox
                      checked={field.value}
                      onCheckedChange={field.onChange}
                    />
                  </FormControl>
                  <FormLabel className="text-sm font-normal">
                    Enable automatic lockout when rules are breached
                  </FormLabel>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>
        </div>

        {/* Hidden preset field */}
        <input type="hidden" {...form.register('preset')} />

        {/* ---- Actions ---- */}
        <div className="flex gap-2 pt-2">
          <Button type="submit" disabled={isBusy}>
            {isBusy ? 'Saving…' : isEdit ? 'Save Changes' : 'Create Configuration'}
          </Button>
        </div>
      </form>
    </Form>
  );
}
