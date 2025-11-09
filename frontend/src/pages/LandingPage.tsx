import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

export function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-bg-primary via-[#1A1A1D] to-[#0F0F11] text-text-primary overflow-hidden">
      {/* Animated background grid */}
      <div className="fixed inset-0 opacity-20">
        <div className="absolute inset-0" style={{
          backgroundImage: 'linear-gradient(rgba(139, 92, 246, 0.15) 1.5px, transparent 1.5px), linear-gradient(90deg, rgba(139, 92, 246, 0.15) 1.5px, transparent 1.5px)',
          backgroundSize: '50px 50px',
        }} />
      </div>

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-6 py-20">
        <div className="max-w-6xl mx-auto text-center">
          {/* Logo/Title with glow effect */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="mb-8"
          >
            <h1 className="text-8xl font-bold mb-4 bg-gradient-to-r from-accent-purple via-status-active to-accent-purple bg-clip-text text-transparent"
                style={{ textShadow: '0 0 80px rgba(139, 92, 246, 0.5)' }}>
              WEAVE
            </h1>
            <p className="text-2xl text-text-secondary font-light tracking-wide">
              AI-Powered Video Orchestration
            </p>
          </motion.div>

          {/* Main description */}
          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-xl text-text-secondary max-w-3xl mx-auto mb-12 leading-relaxed"
          >
            Turn simple ideas into coherent, long-form video content with AI-driven orchestration.
            Watch as intelligent agents weave together characters, scenes, and storylines in real-time.
          </motion.p>

          {/* CTA Button */}
          <motion.button
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            whileHover={{ scale: 1.05, boxShadow: '0 0 40px rgba(139, 92, 246, 0.6)' }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/studio')}
            className="px-12 py-5 bg-gradient-to-r from-accent-purple to-status-active text-white text-lg font-semibold rounded-xl shadow-lg hover:shadow-accent-purple/50 transition-all duration-300"
            style={{ boxShadow: '0 0 30px rgba(139, 92, 246, 0.4)' }}
          >
            Try It Now →
          </motion.button>

          {/* Scroll indicator */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1, y: [0, 10, 0] }}
            transition={{ duration: 2, repeat: Infinity, delay: 1 }}
            className="mt-20 text-text-tertiary"
          >
            <div className="text-sm mb-2">Discover More</div>
            <div className="w-6 h-10 border-2 border-text-tertiary rounded-full mx-auto relative">
              <div className="w-1.5 h-2 bg-accent-purple rounded-full absolute left-1/2 -translate-x-1/2 top-2" />
            </div>
          </motion.div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="relative py-32 px-6">
        <div className="max-w-6xl mx-auto">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-5xl font-bold text-center mb-6 text-text-primary"
          >
            How Weave Works
          </motion.h2>
          <motion.p
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center text-text-secondary text-lg mb-20 max-w-2xl mx-auto"
          >
            A transparent, agentic approach to video generation—see every step of the creative process
          </motion.p>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Step 1 */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="bg-bg-secondary border border-accent-purple/30 rounded-2xl p-8 hover:border-accent-purple/60 transition-all duration-300"
              style={{ boxShadow: '0 4px 20px rgba(139, 92, 246, 0.1)' }}
            >
              <div className="w-16 h-16 bg-gradient-to-br from-accent-purple to-status-active rounded-xl mb-6 flex items-center justify-center text-3xl font-bold"
                   style={{ boxShadow: '0 0 20px rgba(139, 92, 246, 0.5)' }}>
                1
              </div>
              <h3 className="text-2xl font-semibold mb-4 text-text-primary">Describe Your Vision</h3>
              <p className="text-text-secondary leading-relaxed">
                Start with a simple idea—a character, a scene, or a story concept. The Entry Agent guides you through a conversational intake to capture your vision.
              </p>
            </motion.div>

            {/* Step 2 */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="bg-bg-secondary border border-status-warning/30 rounded-2xl p-8 hover:border-status-warning/60 transition-all duration-300"
              style={{ boxShadow: '0 4px 20px rgba(245, 158, 11, 0.1)' }}
            >
              <div className="w-16 h-16 bg-gradient-to-br from-status-warning to-status-error rounded-xl mb-6 flex items-center justify-center text-3xl font-bold"
                   style={{ boxShadow: '0 0 20px rgba(245, 158, 11, 0.5)' }}>
                2
              </div>
              <h3 className="text-2xl font-semibold mb-4 text-text-primary">Watch Agents Orchestrate</h3>
              <p className="text-text-secondary leading-relaxed">
                See the generation tree unfold in real-time. Specialized agents build characters, craft scenes, and maintain continuity—transparently showing their work.
              </p>
            </motion.div>

            {/* Step 3 */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3 }}
              className="bg-bg-secondary border border-status-success/30 rounded-2xl p-8 hover:border-status-success/60 transition-all duration-300"
              style={{ boxShadow: '0 4px 20px rgba(16, 185, 129, 0.1)' }}
            >
              <div className="w-16 h-16 bg-gradient-to-br from-status-success to-status-active rounded-xl mb-6 flex items-center justify-center text-3xl font-bold"
                   style={{ boxShadow: '0 0 20px rgba(16, 185, 129, 0.5)' }}>
                3
              </div>
              <h3 className="text-2xl font-semibold mb-4 text-text-primary">Refine & Export</h3>
              <p className="text-text-secondary leading-relaxed">
                Edit at any checkpoint, adjust character traits, or modify scenes. The system regenerates with your feedback, maintaining consistency across the entire project.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="relative py-32 px-6 bg-gradient-to-b from-transparent via-bg-secondary/30 to-transparent">
        <div className="max-w-6xl mx-auto">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-5xl font-bold text-center mb-20 text-text-primary"
          >
            Powered by Agentic Intelligence
          </motion.h2>

          <div className="grid md:grid-cols-2 gap-6">
            {[
              {
                icon: '🎭',
                title: 'Character Continuity',
                description: 'Deep character profiles with psychological depth, consistent across all scenes',
                color: 'from-accent-purple/20 to-accent-purple/5',
                borderColor: 'border-accent-purple/30',
              },
              {
                icon: '🌳',
                title: 'Transparent Generation Tree',
                description: 'See every agent, every decision, every checkpoint in real-time visual flow',
                color: 'from-status-active/20 to-status-active/5',
                borderColor: 'border-status-active/30',
              },
              {
                icon: '💬',
                title: 'Interactive Chat Control',
                description: 'Steer the creation with natural language—edit on the fly without starting over',
                color: 'from-status-warning/20 to-status-warning/5',
                borderColor: 'border-status-warning/30',
              },
              {
                icon: '🎬',
                title: 'Scene Orchestration',
                description: 'Cinematography, lighting, transitions—all handled by specialized sub-agents',
                color: 'from-status-success/20 to-status-success/5',
                borderColor: 'border-status-success/30',
              },
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: i % 2 === 0 ? -30 : 30 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className={`bg-gradient-to-br ${feature.color} border ${feature.borderColor} rounded-2xl p-8 hover:scale-[1.02] transition-all duration-300`}
              >
                <div className="text-5xl mb-4">{feature.icon}</div>
                <h3 className="text-2xl font-semibold mb-3 text-text-primary">{feature.title}</h3>
                <p className="text-text-secondary leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="relative py-32 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="bg-gradient-to-br from-bg-secondary via-accent-purple/10 to-bg-secondary border border-accent-purple/30 rounded-3xl p-16"
            style={{ boxShadow: '0 0 60px rgba(139, 92, 246, 0.2)' }}
          >
            <h2 className="text-5xl font-bold mb-6 text-text-primary">Ready to Create?</h2>
            <p className="text-xl text-text-secondary mb-10 leading-relaxed">
              Experience the future of AI video generation.
              <br />
              Watch agents orchestrate your vision in real-time.
            </p>
            <motion.button
              whileHover={{ scale: 1.05, boxShadow: '0 0 50px rgba(139, 92, 246, 0.7)' }}
              whileTap={{ scale: 0.95 }}
              onClick={() => navigate('/studio')}
              className="px-16 py-6 bg-gradient-to-r from-accent-purple to-status-active text-white text-xl font-semibold rounded-xl shadow-lg transition-all duration-300"
              style={{ boxShadow: '0 0 30px rgba(139, 92, 246, 0.5)' }}
            >
              Launch Weave Studio →
            </motion.button>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative py-12 px-6 border-t border-border-subtle">
        <div className="max-w-6xl mx-auto text-center text-text-tertiary">
          <p className="text-sm">
            Weave — AI Orchestration for Long-Form Video Creation
          </p>
          <p className="text-xs mt-2 opacity-60">
            Powered by Anthropic Claude & Advanced Agent Architecture
          </p>
        </div>
      </footer>
    </div>
  );
}
