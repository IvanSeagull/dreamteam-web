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

  const currentFormattedDate = `${dob.getDate()}.${dob.getMonth() + 1}.${dob.getFullYear()}`;
  return `${age} y.o. (${currentFormattedDate})`;
}
