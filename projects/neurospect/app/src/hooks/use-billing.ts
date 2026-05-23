import { useMutation, useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import type {
  CheckoutSessionCreate,
  CheckoutSessionResponse,
  SubscriptionResponse,
} from '@/types/api';

export function useSubscription() {
  return useQuery({
    queryKey: ['billing', 'subscription'],
    queryFn: () => api.get('api/billing/subscription').json<SubscriptionResponse>(),
  });
}

export function useCreateCheckout() {
  return useMutation({
    mutationFn: (body: CheckoutSessionCreate) =>
      api.post('api/billing/checkout', { json: body }).json<CheckoutSessionResponse>(),
    onSuccess: (data) => {
      window.location.href = data.checkout_url;
    },
  });
}
