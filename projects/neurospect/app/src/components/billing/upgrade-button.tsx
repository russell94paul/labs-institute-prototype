import { Button } from '@/components/ui/button';
import { useCreateCheckout } from '@/hooks/use-billing';

interface Props {
  tier: 'mentor' | 'trader';
}

export function UpgradeButton({ tier }: Props) {
  const checkout = useCreateCheckout();

  return (
    <Button
      className="w-full"
      disabled={checkout.isPending}
      onClick={() =>
        checkout.mutate({
          tier,
          success_url: `${window.location.origin}/settings/billing?success=true`,
          cancel_url: `${window.location.origin}/settings/billing`,
        })
      }
    >
      {checkout.isPending ? 'Redirecting...' : `Upgrade to ${tier === 'mentor' ? 'Mentor' : 'Trader'}`}
    </Button>
  );
}
