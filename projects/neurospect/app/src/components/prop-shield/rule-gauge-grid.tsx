import { RuleGauge } from './rule-gauge';
import type { RuleBreachStatus } from '@/types/api';

interface Props {
  rules: RuleBreachStatus[];
}

export function RuleGaugeGrid({ rules }: Props) {
  const activeRules = rules.filter((r) => r.active);

  if (activeRules.length === 0) {
    return (
      <p className="text-sm text-muted-foreground">No rules configured for this account.</p>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {activeRules.map((rule) => (
        <RuleGauge key={rule.rule} rule={rule} />
      ))}
    </div>
  );
}
