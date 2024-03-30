import { expect, test } from "vitest";
import main from "./main";

test("tests are working", () => {
  const result = main();

  expect(result).toEqual(true);
});
