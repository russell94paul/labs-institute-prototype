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
import { Trash2 } from 'lucide-react';
import { useDeletePropConfig } from '@/hooks/use-prop-shield';

interface Props {
  configId: string;
  accountLabel: string;
}

export function DeleteConfigDialog({ configId, accountLabel }: Props) {
  const [open, setOpen] = useState(false);
  const deleteMut = useDeletePropConfig();

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="ghost" size="sm" className="text-destructive">
          <Trash2 className="mr-1 h-4 w-4" />
          Delete
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Delete Account Config</DialogTitle>
          <DialogDescription>
            Are you sure you want to delete &ldquo;{accountLabel}&rdquo;? This will remove all rules and lockout history for this account. This action cannot be undone.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            variant="destructive"
            disabled={deleteMut.isPending}
            onClick={() => deleteMut.mutate(configId, { onSuccess: () => setOpen(false) })}
          >
            {deleteMut.isPending ? 'Deleting...' : 'Delete'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
