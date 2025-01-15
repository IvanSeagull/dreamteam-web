export function formatDateOfBirth(dateOfBirth: string): string {
  const dob = new Date(dateOfBirth);
  const today = new Date();

  // Calculate age
  let age = today.getFullYear() - dob.getFullYear();
  const isBeforeBirthday =
    today.getMonth() < dob.getMonth() ||
    (today.getMonth() === dob.getMonth() && today.getDate() < dob.getDate());
  if (isBeforeBirthday) {
    age--;
  }

  const currentFormattedDate = `${today.getDate()}.${today.getMonth() + 1}.${today.getFullYear()}`;
  return `${age} y.o. (${currentFormattedDate})`;
}
