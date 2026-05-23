import { useState } from 'react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { useResetLockout } from '@/hooks/use-prop-shield';

interface Props {
  configId: string;
  currentState: string;
}

export function ResetLockoutDialog({ configId, currentState }: Props) {
  const [open, setOpen] = useState(false);
  const [note, setNote] = useState('');
  const reset = useResetLockout(configId);

  const handleReset = () => {
    reset.mutate(
      { note: note.trim() || null },
      { onSuccess: () => { setOpen(false); setNote(''); } },
    );
  };

  if (currentState === 'none') return null;

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm">Reset Lockout</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Reset Lockout</DialogTitle>
          <DialogDescription>
            This will reset the lockout state to Clear. You should only do this after reviewing why the lockout was triggered.
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-2">
          <Label htmlFor="reset-note">Note (optional)</Label>
          <Textarea
            id="reset-note"
            placeholder="Why are you resetting this lockout?"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            rows={3}
          />
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)}>Cancel</Button>
          <Button onClick={handleReset} disabled={reset.isPending}>
            {reset.isPending ? 'Resetting...' : 'Confirm Reset'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
