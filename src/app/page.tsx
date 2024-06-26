export const metadata = {
  title: "CPP GE Recommender Home ",
  description: `Home page for CPP GE Recommender, 
    containing what this project aims to do and how to use it.`,
};

export default async function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center bg-neutral-900 p-3">
      <h1 className="text-center text-4xl text-white">CPP GE Recommender</h1>
    </main>
  );
}
