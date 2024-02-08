function checkUrl(string) {
  try {
    new URL(string);
  } catch (error) {
    return false;
  }
  return true;
}

module.exports = { checkUrl };
