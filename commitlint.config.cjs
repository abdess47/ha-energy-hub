/**
 * Commit message rules, loaded by the `commit-msg` pre-commit hook.
 *
 * CommonJS on purpose: package.json declares "type": "module", so a `.js` file
 * using `module.exports` throws "module is not defined in ES module scope".
 *
 * The rules of @commitlint/config-conventional are inlined instead of being
 * extended: the hook runs from the repository root, where that package is not
 * installed, so `extends` failed with MODULE_NOT_FOUND. This way the hook works
 * on a fresh clone with no `npm install`, and the rule set is visible here.
 */
module.exports = {
  rules: {
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'chore', 'docs', 'style', 'refactor', 'perf', 'test', 'build', 'ci', 'revert'],
    ],
    'type-case': [2, 'always', 'lower-case'],
    'type-empty': [2, 'never'],
    'scope-case': [2, 'always', 'lower-case'],
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],
    'subject-case': [2, 'never', ['upper-case', 'pascal-case', 'start-case']],
    'header-max-length': [2, 'always', 72],
    'body-leading-blank': [1, 'always'],
    'footer-leading-blank': [1, 'always'],
  },
};
