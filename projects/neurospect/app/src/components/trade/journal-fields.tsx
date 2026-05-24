import type { Control } from 'react-hook-form';
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Checkbox } from '@/components/ui/checkbox';
import { Textarea } from '@/components/ui/textarea';
import { cn } from '@/lib/utils';
import type { TradeFormValues } from './trade-form';

// ICT pre-trade checklist items
const CHECKLIST_ITEMS: { id: string; label: string }[] = [
  { id: 'htf_bias_confirmed', label: 'HTF bias confirmed' },
  { id: 'fvg_identified', label: 'FVG / PDA identified' },
  { id: 'session_correct', label: 'Correct session / kill zone' },
  { id: 'risk_defined', label: 'Risk defined (stop + target)' },
  { id: 'no_conflicting_news', label: 'No conflicting news' },
  { id: 'displacement_confirmed', label: 'Displacement quality confirmed' },
  { id: 'draw_identified', label: 'Draw on liquidity identified' },
];

const EMOTION_OPTIONS: { value: string; label: string; color: string }[] = [
  { value: 'confident', label: 'Confident', color: 'border-green-400 data-[state=checked]:bg-green-100 dark:data-[state=checked]:bg-green-900/30' },
  { value: 'patient', label: 'Patient', color: 'border-blue-400 data-[state=checked]:bg-blue-100 dark:data-[state=checked]:bg-blue-900/30' },
  { value: 'fearful', label: 'Fearful', color: 'border-amber-400 data-[state=checked]:bg-amber-100 dark:data-[state=checked]:bg-amber-900/30' },
  { value: 'greedy', label: 'Greedy', color: 'border-orange-400 data-[state=checked]:bg-orange-100 dark:data-[state=checked]:bg-orange-900/30' },
  { value: 'impulsive', label: 'Impulsive', color: 'border-red-400 data-[state=checked]:bg-red-100 dark:data-[state=checked]:bg-red-900/30' },
  { value: 'revenge', label: 'Revenge', color: 'border-red-600 data-[state=checked]:bg-red-100 dark:data-[state=checked]:bg-red-900/30' },
];

interface Props {
  control: Control<TradeFormValues>;
}

export function JournalFields({ control }: Props) {
  return (
    <div className="space-y-6">
      {/* Pre-trade Checklist */}
      <FormField
        control={control}
        name="pre_trade_checklist"
        render={({ field }) => {
          const checklist: Record<string, boolean> = (field.value as Record<string, boolean>) ?? {};
          return (
            <FormItem>
              <FormLabel>Pre-Trade Checklist</FormLabel>
              <div className="mt-2 grid grid-cols-1 gap-2 sm:grid-cols-2">
                {CHECKLIST_ITEMS.map(({ id, label }) => (
                  <div key={id} className="flex items-center gap-2">
                    <Checkbox
                      id={`checklist-${id}`}
                      checked={checklist[id] ?? false}
                      onCheckedChange={(checked) =>
                        field.onChange({ ...checklist, [id]: !!checked })
                      }
                    />
                    <label
                      htmlFor={`checklist-${id}`}
                      className="cursor-pointer text-sm font-normal"
                    >
                      {label}
                    </label>
                  </div>
                ))}
              </div>
              <FormMessage />
            </FormItem>
          );
        }}
      />

      {/* Emotion Tags */}
      <FormField
        control={control}
        name="emotion_tags"
        render={({ field }) => {
          const tags: string[] = field.value ?? [];
          const toggle = (val: string) => {
            if (tags.includes(val)) {
              field.onChange(tags.filter((t) => t !== val));
            } else {
              field.onChange([...tags, val]);
            }
          };
          return (
            <FormItem>
              <FormLabel>Emotional State</FormLabel>
              <div className="mt-2 flex flex-wrap gap-2">
                {EMOTION_OPTIONS.map(({ value, label, color }) => {
                  const active = tags.includes(value);
                  return (
                    <button
                      key={value}
                      type="button"
                      onClick={() => toggle(value)}
                      className={cn(
                        'rounded-full border px-3 py-1 text-xs font-medium transition-colors',
                        active
                          ? cn('border-2', color, 'font-semibold')
                          : 'border-muted text-muted-foreground hover:border-foreground'
                      )}
                    >
                      {label}
                    </button>
                  );
                })}
              </div>
              <FormMessage />
            </FormItem>
          );
        }}
      />

      {/* Setup Notes */}
      <FormField
        control={control}
        name="setup_notes"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Setup Notes</FormLabel>
            <FormControl>
              <Textarea
                {...field}
                value={field.value ?? ''}
                placeholder="What was the setup? Why did you take it?"
                rows={2}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />

      {/* Execution Notes */}
      <FormField
        control={control}
        name="execution_notes"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Execution Notes</FormLabel>
            <FormControl>
              <Textarea
                {...field}
                value={field.value ?? ''}
                placeholder="How did you execute? Entry quality?"
                rows={2}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />

      {/* Risk Notes */}
      <FormField
        control={control}
        name="risk_notes"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Risk Notes</FormLabel>
            <FormControl>
              <Textarea
                {...field}
                value={field.value ?? ''}
                placeholder="Did you respect your risk? Any sizing issues?"
                rows={2}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />

      {/* Psychology Notes */}
      <FormField
        control={control}
        name="psychology_notes"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Psychology Notes</FormLabel>
            <FormControl>
              <Textarea
                {...field}
                value={field.value ?? ''}
                placeholder="What was your mental state? Did emotions affect your trading?"
                rows={2}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />

      {/* Lesson Learned */}
      <FormField
        control={control}
        name="lesson_learned"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Lesson Learned</FormLabel>
            <FormControl>
              <Textarea
                {...field}
                value={field.value ?? ''}
                placeholder="What will you do differently next time?"
                rows={2}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
    </div>
  );
}
