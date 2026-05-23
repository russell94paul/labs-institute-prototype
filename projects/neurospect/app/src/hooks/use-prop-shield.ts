import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { api } from '@/lib/api';
import type {
  PropFirmPreset,
  PropRuleConfigCreate,
  PropRuleConfigUpdate,
  PropRuleConfigResponse,
  PropShieldStatus,
  LockoutResetRequest,
  PropLockoutEventResponse,
} from '@/types/api';

export function usePresets() {
  return useQuery({
    queryKey: ['prop-shield', 'presets'],
    queryFn: () => api.get('api/prop-shield/presets').json<PropFirmPreset[]>(),
  });
}

export function usePropConfigs() {
  return useQuery({
    queryKey: ['prop-shield', 'configs'],
    queryFn: () => api.get('api/prop-shield/configs').json<PropRuleConfigResponse[]>(),
  });
}

export function usePropConfig(id: string | undefined) {
  return useQuery({
    queryKey: ['prop-shield', 'config', id],
    queryFn: () => api.get(`api/prop-shield/configs/${id}`).json<PropRuleConfigResponse>(),
    enabled: !!id,
  });
}

export function usePropStatus(id: string | undefined) {
  return useQuery({
    queryKey: ['prop-shield', 'status', id],
    queryFn: () => api.get(`api/prop-shield/configs/${id}/status`).json<PropShieldStatus>(),
    enabled: !!id,
    refetchInterval: 30_000,
  });
}

export function useLockoutHistory(id: string | undefined, limit = 50) {
  return useQuery({
    queryKey: ['prop-shield', 'lockout-history', id],
    queryFn: () =>
      api
        .get(`api/prop-shield/configs/${id}/lockout-history`, {
          searchParams: { limit: String(limit) },
        })
        .json<PropLockoutEventResponse[]>(),
    enabled: !!id,
  });
}

export function useCreatePropConfig() {
  const qc = useQueryClient();
  const navigate = useNavigate();
  return useMutation({
    mutationFn: (body: PropRuleConfigCreate) =>
      api.post('api/prop-shield/configs', { json: body }).json<PropRuleConfigResponse>(),
    onSuccess: (data) => {
      qc.invalidateQueries({ queryKey: ['prop-shield', 'configs'] });
      navigate(`/prop-shield/${data.id}`);
    },
  });
}

export function useUpdatePropConfig(id: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: PropRuleConfigUpdate) =>
      api.patch(`api/prop-shield/configs/${id}`, { json: body }).json<PropRuleConfigResponse>(),
    onSuccess: (updated) => {
      qc.setQueryData(['prop-shield', 'config', id], updated);
      qc.invalidateQueries({ queryKey: ['prop-shield', 'configs'] });
    },
  });
}

export function useDeletePropConfig() {
  const qc = useQueryClient();
  const navigate = useNavigate();
  return useMutation({
    mutationFn: (id: string) => api.delete(`api/prop-shield/configs/${id}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['prop-shield', 'configs'] });
      navigate('/prop-shield');
    },
  });
}

export function useResetLockout(configId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: LockoutResetRequest) =>
      api.post(`api/prop-shield/configs/${configId}/reset-lockout`, { json: body }).json(),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['prop-shield', 'config', configId] });
      qc.invalidateQueries({ queryKey: ['prop-shield', 'status', configId] });
      qc.invalidateQueries({ queryKey: ['prop-shield', 'lockout-history', configId] });
    },
  });
}

export function useApplyTilt(configId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (params: { loss_streak: string; revenge_detected: string }) =>
      api
        .post(`api/prop-shield/configs/${configId}/apply-tilt`, {
          searchParams: params,
        })
        .json(),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['prop-shield', 'config', configId] });
      qc.invalidateQueries({ queryKey: ['prop-shield', 'status', configId] });
    },
  });
}
