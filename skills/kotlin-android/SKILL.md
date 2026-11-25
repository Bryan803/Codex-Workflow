---
name: kotlin-android
description: Stack notes for Kotlin/Android work - Jetpack Compose (Material 3), ViewModels and state, coroutines/Flow, Room and migrations, Gradle, and running unit/device tests efficiently. Load before writing or testing Kotlin/Android code.
---

# Kotlin / Android

Project conventions (CLAUDE.md/AGENTS.md, existing code) win over anything here.

## Compose UI
- State hoisting: screens take state + event lambdas; ViewModel exposes `StateFlow<UiState>`, collected with `collectAsStateWithLifecycle()`.
- Use the project's theme tokens (`MaterialTheme.colorScheme`, typography, shared components) instead of hard-coded colors/sizes.
- Every interactive element: content description or semantics, 48dp minimum touch target. Check large font scale (1.3-2.0) and narrow widths (320-360dp) for clipping.
- Add `@Preview`s for the states you build (empty, loading, error, filled, dark) when the project uses previews.
- `Modifier` is the first optional parameter. Keep `remember`/`LaunchedEffect` keys correct.

## Coroutines / Flow
- `viewModelScope` in ViewModels, injected dispatchers for testability, no `GlobalScope`.
- Read-modify-write on stored data happens inside one transaction (`db.withTransaction`) to avoid stale-row races.
- Tests: `runTest` + a test dispatcher; Turbine for flows if the project has it.

## Room
- Schema change = version bump + `Migration` + exported schema JSON updated. Never `fallbackToDestructiveMigration` on user data.
- Test migrations with `MigrationTestHelper`: create old version with data, migrate, assert data survived.

## Gradle and tests (they are slow; run the narrowest thing)
- Unit: `./gradlew testDebugUnitTest --tests 'pkg.ClassTest'` while iterating; the full suite at task/phase end.
- Compile-check device tests without a device: `./gradlew compileDebugAndroidTestKotlin`.
- Device tests: run only the touched classes (`-Pandroid.testInstrumentationRunnerArguments.class=pkg.ClassTest`) unless a full run is asked for; use the project's device script/managed device if it has one.
- A hook puts a time limit on Gradle/adb/emulator commands (45 min): it hands you a wrapped command that writes output to a log; run that. On TIMED OUT, report it; check `adb devices` / emulator boot before blaming code.
- Don't run two Gradle builds in the same project at once.
- Lint: `./gradlew lintDebug`; compare warning count to the baseline instead of fixing unrelated warnings.
