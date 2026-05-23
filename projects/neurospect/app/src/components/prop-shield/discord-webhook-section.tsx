import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Bell, Check, X } from 'lucide-react';
import { useUpdatePropConfig } from '@/hooks/use-prop-shield';

interface Props {
  configId: string;
  currentUrl: string | null;
}

export function DiscordWebhookSection({ configId, currentUrl }: Props) {
  const [editing, setEditing] = useState(false);
  const [url, setUrl] = useState(currentUrl ?? '');
  const update = useUpdatePropConfig(configId);

  const handleSave = () => {
    update.mutate(
      { discord_webhook_url: url.trim() || null },
      { onSuccess: () => setEditing(false) },
    );
  };

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2">
        <Bell className="h-4 w-4 text-muted-foreground" />
        <Label className="text-sm font-medium">Discord Alerts</Label>
      </div>
      {editing ? (
        <div className="flex gap-2">
          <Input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://discord.com/api/webhooks/..."
            className="flex-1"
          />
          <Button size="icon" variant="ghost" onClick={handleSave} disabled={update.isPending}>
            <Check className="h-4 w-4" />
          </Button>
          <Button size="icon" variant="ghost" onClick={() => { setEditing(false); setUrl(currentUrl ?? ''); }}>
            <X className="h-4 w-4" />
          </Button>
        </div>
      ) : (
        <div className="flex items-center gap-2">
          <p className="text-sm text-muted-foreground">
            {currentUrl ? 'Webhook configured' : 'No webhook configured'}
          </p>
          <Button variant="link" size="sm" className="h-auto p-0" onClick={() => setEditing(true)}>
            {currentUrl ? 'Edit' : 'Add'}
          </Button>
        </div>
      )}
    </div>
  );
}
