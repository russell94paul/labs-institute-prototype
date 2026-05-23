import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { PresetPicker } from '@/components/prop-shield/preset-picker';
import { ConfigForm } from '@/components/prop-shield/config-form';
import type { PropFirmPreset } from '@/types/api';

type Step = 'pick' | 'form';

export function PropShieldNewPage() {
  const [step, setStep] = useState<Step>('pick');
  const [presetValues, setPresetValues] = useState<Record<string, unknown> | undefined>();

  const handlePresetSelect = (preset: PropFirmPreset | null) => {
    if (preset) {
      setPresetValues({
        account_label: `${preset.firm_name} ${preset.account_size}`,
        account_type: 'eval' as const,
        preset: preset.preset_id,
        account_balance:
          parseFloat(preset.account_size.replace(/[^0-9.]/g, '')) * 1000 || 0,
        daily_loss_limit: preset.daily_loss_limit,
        trailing_drawdown_limit: preset.trailing_drawdown_limit,
        max_contracts: preset.max_contracts,
        max_daily_trades: preset.max_daily_trades,
        consistency_rule_pct: preset.consistency_rule_pct,
      });
    } else {
      setPresetValues(undefined);
    }
    setStep('form');
  };

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center gap-3">
        {step === 'form' ? (
          <Button variant="ghost" size="icon" onClick={() => setStep('pick')}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
        ) : (
          <Button variant="ghost" size="icon" asChild>
            <Link to="/prop-shield">
              <ArrowLeft className="h-4 w-4" />
            </Link>
          </Button>
        )}
        <h1 className="text-2xl font-semibold">
          {step === 'pick' ? 'Choose a Preset' : 'New Prop Account'}
        </h1>
      </div>

      {step === 'pick' ? (
        <PresetPicker onSelect={handlePresetSelect} />
      ) : (
        <ConfigForm presetValues={presetValues} />
      )}
    </div>
  );
}
