export type Language = 'en' | 'hi' | 'pa' | 'ml';
const en = {
  ai_powered: 'AI powered', area_hectare: 'Area (hectares)', carbon_credits: 'Carbon credits',
  chat_greeting: 'Hello! I am your crop assistant. Ask me about crop health, irrigation, or soil care.',
  chat_input: 'Ask a farming question…', clear_history: 'Clear conversation', credits_earned: 'Estimated credits',
  crop_assistant: 'Crop assistant', crop_type: 'Crop type', data_analytics: 'Data analytics',
  field_log: 'Field log', indices_report: 'Vegetation indices', irrigation_placeholder: 'Select irrigation method',
  irrigation_type: 'Irrigation type', market_price: 'Market price', methane_reduction: 'Methane reduction',
  my_field: 'My field', quick_crop_health: 'How can I check my crop health?',
  quick_fertilizer: 'How should I plan fertilizer use?', quick_weather: 'How does weather affect irrigation?',
  select_crop: 'Select crop', soil_placeholder: 'Select soil type', soil_type: 'Soil type',
  tree_count: 'Tree count', view_directions: 'View directions', water_saving: 'Water savings',
};
export type TranslationKey = keyof typeof en;
// English fallback until each locale has a reviewed translation catalog.
export const translations: Record<Language, Partial<Record<TranslationKey, string>>> = { en, hi: {}, pa: {}, ml: {} };
