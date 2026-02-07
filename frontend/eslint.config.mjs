// frontend/eslint.config.mjs
import withNuxt from "./.nuxt/eslint.config.mjs";

export default withNuxt({
  // We can add custom rules here if we want
  rules: {
    // Optional: Nuxt pages often have single-word names (like 'index' or 'feed'),
    // so we turn off this strict Vue rule to stop it from yelling at us.
    "vue/multi-word-component-names": "off",

    // Optional: Warn about unused variables instead of erroring
    "@typescript-eslint/no-unused-vars": "warn",
  },
});
