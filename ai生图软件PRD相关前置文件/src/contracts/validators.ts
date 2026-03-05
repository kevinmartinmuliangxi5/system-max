import { z } from 'zod';

const PromptMessageSchema = z.object({
  content: z.string().min(1),
});

const PromptChoiceSchema = z.object({
  message: PromptMessageSchema,
});

export const PromptEnhanceResponseSchema = z.object({
  id: z.string(),
  choices: z.array(PromptChoiceSchema).min(1),
});

export const ImageResponseSchema = z.object({
  data: z.array(
    z
      .object({
        b64_json: z.string().min(1).optional(),
        url: z.string().min(1).optional(),
      })
      .refine((item) => Boolean(item.b64_json || item.url), {
        message: 'Image item must contain b64_json or url',
      })
  ).min(1),
});

const ErrorPayloadSchema = z.object({
  code: z.string(),
  message: z.string().min(1),
});

export const ErrorResponseSchema = z.object({
  error: ErrorPayloadSchema,
});

export type PromptEnhanceResponse = z.infer<typeof PromptEnhanceResponseSchema>;
export type ImageResponse = z.infer<typeof ImageResponseSchema>;
export type ErrorResponse = z.infer<typeof ErrorResponseSchema>;

export function validatePromptEnhanceResponse(input: unknown): PromptEnhanceResponse {
  return PromptEnhanceResponseSchema.parse(input);
}

export function validateImageResponse(input: unknown): ImageResponse {
  return ImageResponseSchema.parse(input);
}

export function validateErrorResponse(input: unknown): ErrorResponse {
  return ErrorResponseSchema.parse(input);
}
