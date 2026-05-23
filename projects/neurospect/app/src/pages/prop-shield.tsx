import { Link } from 'react-router-dom';
import { Plus, Shield } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { usePropConfigs } from '@/hooks/use-prop-shield';
import { ConfigCard } from '@/components/prop-shield/config-card';

export function PropShieldPage() {
  const { data: configs, isLoading } = usePropConfigs();

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Prop Shield</h1>
        <Button asChild size="sm">
          <Link to="/prop-shield/new">
            <Plus className="mr-1 h-4 w-4" />
            New Account
          </Link>
        </Button>
      </div>

      {isLoading ? (
        <div className="flex flex-col gap-3">
          {Array.from({ length: 3 }).map((_, i) => (
            <Skeleton key={i} className="h-24 w-full rounded-lg" />
          ))}
        </div>
      ) : !configs || configs.length === 0 ? (
        <div className="flex flex-col items-center justify-center gap-4 py-24">
          <Shield className="h-12 w-12 text-muted-foreground" />
          <p className="max-w-sm text-center text-muted-foreground">
            Add your first prop firm account to start tracking rules and protecting your funded
            status.
          </p>
          <Button asChild>
            <Link to="/prop-shield/new">Add Your First Account</Link>
          </Button>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {configs.map((config) => (
            <ConfigCard key={config.id} config={config} />
          ))}
        </div>
      )}
    </div>
  );
}
